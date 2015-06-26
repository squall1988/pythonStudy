/*
 * =====================================================================================
 *
 *       Filename:  test.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  2015/06/26 16时45分05秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */

#include <stdio.h>
extern "C" {

  extern float test_python(float *array, int len) {
    for (int i = 0; i < len; i++) {
      printf("%f\n", array[i]);
    }
    return 1.0;
  }
}
