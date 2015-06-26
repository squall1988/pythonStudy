# Python和C语言混合编程

众所周知，C语言基本上是效率最高的一种语言，但是又有一些比较让人头疼的问题。
比如C语言没有非常现代化的字符串处理库，这样就导致一在处理一些字符串相关的东西的时候非常不方便，
一些底层的库都是直接使用C语言进行编写，这样可以保证程序以非常高效的方式运行，但是也面临一些问题，
即除了核心代码以外还有其他非常多的打杂的代码，同时，C语言中包含了非常多的指针等操作，这样就导致接口并不会非常的友好，
这种情况下我们需要一种胶水语言将不同模块之间联通起来，Python作为一种胶水语言是可以非常方便的满足这样的需求，这样
这样程序猿就可以关注在最核心的模块的编写，而把一些外围的代码交给Python来做。

``` python
import numpy as np
import ctypes as ct

clib = ct.CDLL('./test.so')
clib.test_python()
```

```c
#include <stdio.h>

extern void test_python() {
  printf("this is a test in c");
}
```

```Makefile
CC=gcc
test.so: main.c
  $(CC) $^ -fPIC -shared -o $@
```

这样我们就完成了一个最简单的Python和C语言的混合编程样例。
在这里我们解释一下，我们做了什么事情，首先我们使用C语言写了一个最简单的
程序，将这个模块编译成动态链接库，在Python中，我们使用ctypes库载入对应的
动态链接库，然后我们就可以调用动态链接库里面暴漏出来的接口了。
需要注意各个平台下的写法是不一样的，在windows平台下，需要使用__dllexport宏
来告诉编译器，将这个函数暴露出来。

我们再来看一个例子，主要是使用带有参数的函数，
```c

#include <stdio.h>

extern void test_python(float \*array, int len) {
  for (int i = 0; i < len; i++) {
    printf("%f\n", array[i]);
  }
}
```

```python
import numpy as np
import ctypes as ct

clib = ct.CDLL('./test.so')
a = [1.0, 2.0, 3.0]
clib.test_python((ct.c_float*len(a))(*a), ct.c_int(len(a)))

```
这样我们就把一个Python的传递进了一个C语言的函数中去。
需要注意的是当我们使用g++或者clang++作为来编译C代码的时候，需要在外围加上对应的extern "C"声明。

上面的那种写法是非常丑陋的，还有另外一种更方便的方式把数据传入进模块中。

```python

import numpy as np
import numpy as np
import ctypes as ct

clib = ct.CDLL('./test.so')
a = np.array([1,2,3], dtype=np.float32, copy=True)
clib.test_python(a.ctypes.data_as(ct.POINTER(ct.c_float)), a.shape[0])
```

在考虑另外一种情况，我们会返回最终的结果码来说明程序运行是否成功。
这个时候需要我们使用指定返回的数据类型。

```c
#include <stdio.h>

extern int test_python(float \*array, int len) {
  for (int i = 0; i < len; i++) {
    printf("%f\n", array[i]);
  }
  return 0;
}
```

```python

import numpy as np
import numpy as np
import ctypes as ct

clib = ct.CDLL('./test.so')
a = np.array([1,2,3], dtype=np.float32, copy=True)
clib.test_python.restype = ct.c_int
clib_result = clib.test_python(a.ctypes.data_as(ct.POINTER(ct.c_float)), a.shape[0])
print clib_result
```
