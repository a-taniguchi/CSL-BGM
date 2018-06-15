#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "./opencv_lib.hpp"
#include <opencv2/imgcodecs.hpp>
//http://opencv.jp/cookbook/opencv_img.html

//実行は、「./henkan 3」のようにコマンド引数をつける
int main(int argc, char *argv[])
{
  char filename[64];
  int object_num = atoi(argv[1]);
  for (int i=1;i <= object_num;i++){
    //sprintf(filename,"./image/label_%02d.ppm",i);//
    sprintf(filename,"./image/00000005.ppm");//test
    cv::Mat src_img = cv::imread(filename, 1);
    if(src_img.empty()) return -1;
    //左上、左下、右下、右上（ｘ，ｙ）
    cv::Point2f pts1[] = {cv::Point2f(107,50), cv::Point2f(-11,232), cv::Point2f(408,232),cv::Point2f(263,50)};
    cv::Point2f pts2[] = {cv::Point2f(0,0),cv::Point2f(0,200),cv::Point2f(200,200),cv::Point2f(200,0)};
    // r5014以前ではノイズがのります．
    //cv::Point2f pts1[] = {cv::Point2f(150,150.),cv::Point2f(150,300.),cv::Point2f(350,300.),cv::Point2f(350,150.)};
    //cv::Point2f pts2[] = {cv::Point2f(200,200.),cv::Point2f(150,300.),cv::Point2f(350,300.),cv::Point2f(300,200.)};
    
    // 透視変換行列を計算
    cv::Mat perspective_matrix = cv::getPerspectiveTransform(pts1, pts2);
    cv::Mat dst_img;
    // 変換
    cv::warpPerspective(src_img, dst_img, perspective_matrix, src_img.size(), cv::INTER_LINEAR);
    
    
    // 変換前後の座標を描画
    cv::line(src_img, pts1[0], pts1[1], cv::Scalar(255,255,0), 1, CV_AA);
    cv::line(src_img, pts1[1], pts1[2], cv::Scalar(255,255,0), 1, CV_AA);
    cv::line(src_img, pts1[2], pts1[3], cv::Scalar(255,255,0), 1, CV_AA);
    cv::line(src_img, pts1[3], pts1[0], cv::Scalar(255,255,0), 1, CV_AA);
    cv::line(src_img, pts2[0], pts2[1], cv::Scalar(255,0,255), 1, CV_AA);
    cv::line(src_img, pts2[1], pts2[2], cv::Scalar(255,0,255), 1, CV_AA);
    cv::line(src_img, pts2[2], pts2[3], cv::Scalar(255,0,255), 1, CV_AA);
    cv::line(src_img, pts2[3], pts2[0], cv::Scalar(255,0,255), 1, CV_AA);
    
    cv::circle(dst_img, cv::Point2f(100,100),100, cv::Scalar(0,0,0), 1, CV_AA,0);

    cv::namedWindow("src", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
    cv::namedWindow("dst", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
    cv::imshow("src", src_img);
    cv::imshow("dst", dst_img);
    
    //sprintf(filename,"./image/henkan_%02d.ppm",i);//
    sprintf(filename,"./image/henkan1.png");//test
    cv::imwrite(filename,dst_img);
    sprintf(filename,"./image/henkan2.png");//test
    cv::imwrite(filename,src_img);
  }
  cv::waitKey(0);
}
