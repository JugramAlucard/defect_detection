#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

Mat searchConcaveRegion(vector<vector<Point> >hull, Mat &src);
vector<Point2f> searchConcavePoint(Mat &src);

int main()
{
	Mat img = imread("concave.png", 1);
	Mat gray, gray_back;

	cvtColor(img, gray, COLOR_BGR2GRAY);

	threshold(gray, gray, 0, 255, THRESH_OTSU);
	gray_back = gray.clone();

	//提取轮廓
	vector<vector<Point>>contours;
	findContours(gray, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_NONE);
	drawContours(img, contours, -1, Scalar(0, 0, 255), 2);

	Mat aotu = searchConcaveRegion(contours, gray_back);
	vector<Point2f> pt;
	pt = searchConcavePoint(aotu);

	line(img, pt[pt.size() - 2], pt[pt.size() - 1], Scalar(255, 0, 0), 2, 8, 0);

	imshow("seg_line", img);
	waitKey(0);
}

/**
* @brief searchConcaveRegion 寻找凹区域
* @param hull  凸包点集
* @param src  原图像（二值图）
* @return 返回 图像凹区域
*/
Mat searchConcaveRegion(vector<vector<Point> >contours, Mat &src)
{
	if (src.empty())
		return Mat();

	//遍历每个轮廓，寻找其凸包
	vector<vector<Point>>hull(contours.size());
	for (unsigned int i = 0; i < contours.size(); ++i)
	{
		convexHull(Mat(contours[i]), hull[i], false);
	}

	//绘制轮廓及其凸包
	Mat drawing = Mat::zeros(src.rows, src.cols, CV_8UC1);
	for (unsigned int i = 0; i < contours.size(); ++i)
	{
		drawContours(drawing, hull, i, Scalar(255), -1, 8, vector<Vec4i>(), 0, Point());
		drawContours(drawing, contours, i, Scalar(0), -1, 8, vector<Vec4i>(), 0, Point());
	}

	medianBlur(drawing, drawing, 3);

	imshow("roi_area", drawing);

	return drawing;
}

/**
* @brief searchConcavePoint
* @param src 凹区域图像
* @return 返回匹配好的凹点对（2个）
*/
vector<Point2f> searchConcavePoint(Mat &src)
{
	vector<Point2f> ConcavePoint;
	//轮廓寻找
	vector<vector<Point> > contour;//用来存储轮廓
	vector<Vec4i> hierarchys;
	findContours(src, contour, hierarchys,
		cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE, Point(0, 0));  //寻找轮廓

	//凹区域少于2要退出
	if (contour.size() < 2)
		return ConcavePoint;

	//按照轮廓面积大小排序
	sort(contour.begin(), contour.end(), [](const vector<Point> &s1,
		const vector<Point> &s2) {
		double a1 = contourArea(s1);
		double a2 = contourArea(s2);
		return a1 > a2;
	});

	int minDistance = 100000000;//最短距离
	for (int i = 0; i < contour[0].size(); ++i)
		for (int j = 0; j < contour[1].size(); ++j)
		{
			//欧氏距离
			int d = sqrt(pow((contour[0][i].x - contour[1][j].x), 2) +
				pow((contour[0][i].y - contour[1][j].y), 2));
			if (minDistance > d)
			{
				minDistance = d;
				ConcavePoint.push_back(contour[0][i]);
				ConcavePoint.push_back(contour[1][j]);
			}
		}
	cout << "ConcavePoint0:" << ConcavePoint[ConcavePoint.size() - 2].x << "," << ConcavePoint[ConcavePoint.size() - 2].y << endl;
	cout << "ConcavePoint1:" << ConcavePoint[ConcavePoint.size() - 1].x << "," << ConcavePoint[ConcavePoint.size() - 1].y << endl;

	return ConcavePoint;
}