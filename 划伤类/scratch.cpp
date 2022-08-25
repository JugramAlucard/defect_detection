#include <iostream>
#include <opencv2\imgcodecs.hpp>
#include <opencv2\core.hpp>
#include <opencv2\imgproc.hpp>
#include <opencv2\highgui.hpp>

using namespace cv;

int main()
{
	std::string strImgFile = "D:\\mvi\\crack.png";
	Mat mSrc = imread(strImgFile);
	CV_Assert(!mSrc.empty());

	resize(mSrc, mSrc, Size(mSrc.cols / 2, mSrc.rows / 2));

	Mat mGray;
	cvtColor(mSrc, mGray, COLOR_BGR2GRAY);
	CV_Assert(!mGray.empty());

	GaussianBlur(mGray, mGray, Size(5, 5), -1);

	Mat mMean;
	blur(mGray, mMean, Size(15, 15));
	CV_Assert(!mMean.empty());

	Mat mDiff;
	absdiff(mMean, mGray, mDiff);
	CV_Assert(!mDiff.empty());

	imshow("diff", mDiff);

	Mat mThresh;
	threshold(mDiff, mThresh, 5, 255, THRESH_BINARY);
	CV_Assert(!mThresh.empty());

	imshow("thres", mThresh);

	std::vector<std::vector<Point>> contours;
	findContours(mThresh, contours, RETR_TREE, CHAIN_APPROX_NONE);

	RNG rng;

	Mat mSrcCopy = mSrc.clone();
	for (int i = 0; i < contours.size(); i++)
	{
		RotatedRect rr = minAreaRect(contours[i]);
		float max = rr.size.height > rr.size.width ? rr.size.height : rr.size.width;
		float min = rr.size.height > rr.size.width ? rr.size.width : rr.size.height;

		if (rr.size.area() > 1000 && rr.size.area() < 1000000 &&
			max / min > 3 && max / min < 4)
		{
			/*int b = rng.uniform(0, 256);
			int g = rng.uniform(0, 256);
			int r = rng.uniform(0, 256);
			drawContours(mSrcCopy, contours, i, Scalar(b, g, r));*/
			drawContours(mSrcCopy, contours, i, Scalar(0, 0, 255));
		}
	}

	imshow("contours", mSrcCopy);

	waitKey(0);
	destroyAllWindows();

	return 0;
}
