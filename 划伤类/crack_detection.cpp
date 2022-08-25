#include <opencv2\opencv.hpp>
#include <vector>
#include<time.h> 
#include <tchar.h>

using namespace cv;
using namespace std;

void preProcessing(Mat &srcImg, Mat &binImg, int elementSize = 7)
{
	Mat grayImg;
	cvtColor(srcImg, grayImg, COLOR_RGB2GRAY);
	int blockSize = 25;
	int constValue = 45;
	adaptiveThreshold(grayImg, binImg, 255, cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY_INV, blockSize, constValue);
	Mat element = getStructuringElement(MORPH_RECT, Size(elementSize, elementSize));
	dilate(binImg, binImg, element);
	medianBlur(binImg, binImg, 9);
}

int _tmain(int argc, _TCHAR* argv[])
{
	clock_t start, finish;
	double totaltime;
	start = clock();

	Mat srcImg = imread("concave.png");

	Mat binImg;
	preProcessing(srcImg, binImg);
	imshow("binImg", binImg);

	finish = clock();
	totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
	cout << "\n此程序的运行时间为" << totaltime << "秒！" << endl;

	waitKey();

	return 0;
}