#include <Python.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define INIT_BUFF_SIZE 100

typedef struct dynamicStr {
    char*   str;
    size_t  size;
    size_t  capacity;
}dynamicStr;

int check_is_number(const char* c_value) {
    int flag = 1;
    for(size_t i = 0; i < strlen(c_value); i++) {
        if(!isdigit(c_value[i]) && c_value[i] != '.') {
            flag = 0;
            break;
        }  
    }
    return flag;
}

int check_is_int(const char* c_value) {
    int flag = 1;
    while(*c_value && *c_value != '.') {
        c_value++;
    }
    c_value++;
    while(*c_value && *c_value != '\0') {
        if (*c_value != '0') {
            flag = 0;
            break;
        }
        c_value++;
    }
    return flag;
}

void removeSubstring(char *str, const char *sub) {
    size_t len = strlen(sub);
    while ((str = strstr(str, sub)) != NULL) {
        memmove(str, str + len, strlen(str + len) + 1);
    }
}

void concatenateStrings(dynamicStr* temp, const char *str2) {
    size_t len1 = (size_t)strlen(temp->str);
    size_t len2 = strlen(str2);

    if(temp->capacity <= (len1 + len2)) {
        temp->capacity *= 2;
        temp->str = (char*)realloc(temp->str, temp->capacity);
    }
    temp->size += len2;
    strcat(temp->str, str2);
}

static PyObject* cjson_loads(PyObject* self, PyObject* args) {
    char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument");
        return NULL;
    }

    PyObject *dict = NULL;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }
    char* copy_str = (char*)malloc(sizeof(char)*(strlen(json_str)+1));
    strcpy(copy_str, json_str);

    if(*copy_str != '{') {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        free(copy_str);
        return NULL;
    }

    char* temp = copy_str;
    while(*temp) {
        if(*(temp + 1) == '\0' && *temp != '}') {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            free(copy_str);
            return NULL;
        }
        temp++;
    }

    if (strstr(copy_str, ":") == NULL) {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        free(copy_str);
        return NULL;
    }

    const char sub1[] = "{";
    removeSubstring(copy_str, sub1);
    const char sub2[] = "}";
    removeSubstring(copy_str, sub2);
    const char sub3[] = "\"";
    removeSubstring(copy_str, sub3);

    char *str1, *str2, *token, *subtoken;
    char *saveptr1, *saveptr2;
    int j;
    for (j = 1, str1 = copy_str; ; j++, str1 = NULL) {
        token = strtok_r(str1, ",", &saveptr1);
        if (token == NULL) {
            break;
        }
        if(*token == ' ') {
            token++;
        }
        int counter = 0;
        PyObject *key = NULL;
        PyObject *value = NULL;
        for (str2 = token; ; str2 = NULL) {
            subtoken = strtok_r(str2, ":", &saveptr2);
            if (subtoken == NULL) {
                if(counter < 2) {
                    PyErr_Format(PyExc_TypeError, "Expected object or value");
                    free(copy_str);
                    return NULL;
                }
                break;
            }
            if(counter == 0) {
                if (!(key = Py_BuildValue("s", subtoken))) {
                    printf("ERROR: Failed to build string value\n");
                    free(copy_str);
                    return NULL;
                }
            } else if(counter == 1) {
                while (*subtoken == ' ') {
                    subtoken++;
                }
                if (atof(subtoken) != 0) {
                    if (!(value = Py_BuildValue("d", atof(subtoken)))) {
                        printf("ERROR: Failed to build integer value\n");
                        free(copy_str);
                        return NULL;
                    }
                } else {
                    if (!(value = Py_BuildValue("s", subtoken))) {
                        printf("ERROR: Failed to build string value\n");
                        free(copy_str);
                        return NULL;
                    }
                }
            }
            if (counter == 1) {
                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    free(copy_str);
                    return NULL;
                }
            }
            counter++;
        }
    }
    free(copy_str);
    return dict;
}

static PyObject* cjson_dumps(PyObject* self, PyObject* args) {
    PyObject* input_dict;
    if (!PyArg_ParseTuple(args, "O", &input_dict) || !PyDict_Check(input_dict)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument");
        return NULL;
    }

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    Py_ssize_t pos_for_check = 0;

    dynamicStr result;
    result.size = 0;
    result.capacity = INIT_BUFF_SIZE;
    result.str = (char*)calloc(result.capacity, result.capacity);

    concatenateStrings(&result, "{");

    while (PyDict_Next(input_dict, &pos, &key, &value)) {
        PyObject *str_key = PyObject_Str(key);
        const char *c_key = PyUnicode_AsUTF8(str_key);

        concatenateStrings(&result, "\"");
        concatenateStrings(&result, c_key);
        concatenateStrings(&result, "\": ");

        PyObject* str_value = PyObject_Str(value);
        const char *c_value = PyUnicode_AsUTF8(str_value);

        if(check_is_number(c_value)) {
            if(check_is_int(c_value)) {
                char* istr = strtok(c_value, ".");
                concatenateStrings(&result, istr);
            } else {
                concatenateStrings(&result, c_value);
            } 
        } else {
            concatenateStrings(&result, "\"");
            concatenateStrings(&result, c_value);
            concatenateStrings(&result, "\"");
        }

        pos_for_check = pos;
        if(PyDict_Next(input_dict, &pos_for_check, &key, &value)) {
            concatenateStrings(&result, ", ");
        }
    }
    concatenateStrings(&result, "}");
    char buff[result.capacity];
    strcpy(buff, result.str);
    free(result.str);
    return Py_BuildValue("s", buff);
}

static PyMethodDef cjson_methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Load JSON from a string."},
    {"dumps", cjson_dumps, METH_VARARGS, "Dump JSON to a string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjson = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    cjson_methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson);
}
