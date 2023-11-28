from setuptools import setup, Extension

def main():
    setup(name="cjons",
          version="1.0.1",
          author="M.Gilev",
          ext_modules=[Extension(name="cjson", sources=["cjson.c"])])
    
if __name__ == "__main__":
    main()