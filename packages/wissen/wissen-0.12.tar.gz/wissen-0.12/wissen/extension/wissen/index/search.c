#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int
interpolationsearch (int key, int *base[2], unsigned int num)
{
	int low = 0;              
	int high = num - 1;
	int mid;
	
	while (base [low][0] < key && base [high][0] >= key) {
		mid = (int) (low + floor (abs (((key - base [low][0]) * (high - low)) / (base [high] [0] - base [low] [0]))));
		if (base [mid][0] < key) low = mid + 1;
		else if (base [mid][0] > key) high = mid - 1;
		else return mid;
	}
	
	if (base [low][0] == key) return low;
	else return -1;
}

int
binarysearch (int key, int *base [2], unsigned int num)
{
	int low = 0;
	int high = num - 1;
	int mid;
	
	while(low <= high){
		mid = (low + high) / 2;
		if(key == base [mid][0]) return mid;
		else if(key < base [mid][0]) high = mid - 1;
		else low = mid + 1;
	}
	return -1;
}
