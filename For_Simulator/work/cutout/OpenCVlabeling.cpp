//http://qiita.com/wakaba130/items/9d921b8b3eb812e4f197
#include<iostream>
#include<vector>
//#include<random>
//#include<string>
//#include<strstream>
//#include"OpenCV3.h"
#include <opencv/cv.h>
#include <opencv2/opencv.hpp>
//#include <opencv2/core/core.hpp>
//#include <opencv2/nonfree/nonfree.hpp>
//#pragma comment(lib,"opencv_nonfree243.lib")
//#include <opencv2/features2d/features2d.hpp>
//#include <opencv/highgui.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

#include <iostream>
#include <vector>
#include "./opencv_lib.hpp"


int main(void)
{
    char filename[64];
    
    //グレースケール入力
    cv::Mat src = cv::imread("./image/sabun_01.pgm", cv::IMREAD_GRAYSCALE);

    // 画像の読み込みに失敗したらエラー終了する
    if(src.empty())
    {
        std::cerr << "Failed to open image file." << std::endl;
        return -1; 
    }

    //ラべリング処理
    cv::Mat LabelImg;
    cv::Mat stats;
    cv::Mat centroids;
    int nLab = cv::connectedComponentsWithStats(src, LabelImg, stats, centroids);

    // ラベリング結果の描画色を決定
    std::vector<cv::Vec3b> colors(nLab);
    colors[0] = cv::Vec3b(0, 0, 0);
    for (int i = 1; i < nLab; ++i) {
        colors[i] = cv::Vec3b((rand() & 255), (rand() & 255), (rand() & 255));
    }

    // ラベリング結果の描画
    cv::Mat Dst(src.size(), CV_8UC3);
    
    //物体ごとの中心座標を描画
    cv::Mat Obj1(src.size(), CV_8UC3);
    cv::Mat Obj2(src.size(), CV_8UC3);
    cv::Mat Obj3(src.size(), CV_8UC3);
    cv::Mat Obj4(src.size(), CV_8UC3);
    cv::Mat Obj[4] = {Obj1,Obj2,Obj3,Obj4};
    
    for (int i = 0; i < Dst.rows; ++i) {
        int *lb = LabelImg.ptr<int>(i);
        cv::Vec3b *pix = Dst.ptr<cv::Vec3b>(i);
        for (int j = 0; j < Dst.cols; ++j) {
            pix[j] = colors[lb[j]];
        }
    }

    int object_num = 0;
    //ROIの設定
    for (int i = 1; i < nLab; ++i) {
        int *param = stats.ptr<int>(i);
      
        int x = stats.at<int>(i,cv::CC_STAT_LEFT);
        int y = stats.at<int>(i,cv::CC_STAT_TOP);
        int w = stats.at<int>(i,cv::CC_STAT_WIDTH);
        int h = stats.at<int>(i,cv::CC_STAT_HEIGHT);
        int area = stats.at<int>(i,cv::CC_STAT_AREA);
      if(area >= 5){
        object_num++;
	//int x = param[cv::ConnectedComponentsTypes::CC_STAT_LEFT];
	//int y = param[cv::ConnectedComponentsTypes::CC_STAT_TOP];
	//int height = param[cv::ConnectedComponentsTypes::CC_STAT_HEIGHT];
	//int width = param[cv::ConnectedComponentsTypes::CC_STAT_WIDTH];
	
        cv::rectangle(Dst, cv::Rect(x, y, w, h), cv::Scalar(255, 255, 255), 1);
    //}

    //重心の出力
    //for (int i = 1; i < nLab; ++i) {
        //double *param = centroids.ptr<double>(i);
        int x2 = static_cast<int>(x);
        int y2 = static_cast<int>(y);

        cv::circle(Dst,cv::Point(x2 + w/2, y2 + h/2), 2, cv::Scalar(0, 0, 255), -1);

	cv::circle(Obj[i],cv::Point(x2 + w/2, y2 + h/2), 2, cv::Scalar(255, 255, 255), -1);

    //}

    //面積値の出力
    //for (int i = 1; i < nLab; ++i) {
        //int *param = stats.ptr<int>(i);
        std::cout << "area "<< i <<" : " << area << std::endl;

        //ROIの左上に番号を書き込む
        //int x = param[cv::ConnectedComponentsTypes::CC_STAT_LEFT];
        //int y = param[cv::ConnectedComponentsTypes::CC_STAT_TOP];
        std::stringstream num;
        num << i;
        cv::putText(Dst, num.str(), cv::Point(x+5, y+20), cv::FONT_HERSHEY_COMPLEX, 0.5, cv::Scalar(255, 255, 255), 1);
      }
    }

    cv::imshow("Src", src);
    cv::imshow("Labels", Dst);

    sprintf(filename,"./image/label.ppm");//
    //ppm_write(filename, Dst);
    //imwrite(const string& filename, const Mat& img, const vector<int>& params=vector<int>()
    imwrite(filename, Dst);
    for (int i = 1;i<= object_num;i++){
      sprintf(filename,"./image/label_%02d.ppm",i);//
      imwrite(filename, Obj[i]);
    }
    cv::waitKey();

    std::cout << "object num: " << object_num << std::endl;

    return 0;
}
