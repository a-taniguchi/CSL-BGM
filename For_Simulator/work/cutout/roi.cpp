#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "./opencv_lib.hpp"
#include <opencv2/imgcodecs.hpp>

int main()
{
//イメージをロード
IplImage* ipl = ::cvLoadImage("./image/00000001.ppm", CV_LOAD_IMAGE_ANYDEPTH | CV_LOAD_IMAGE_ANYCOLOR);

//x=10, y=10から64x64でROIを設定
::cvSetImageROI(ipl, ::cvRect(10, 10, 64, 64));

//ROIを設定した状態でセーブ
::cvSaveImage("./image/result.ppm", ipl);

//ROIの解除
::cvResetImageROI(ipl);

//イメージの解放
::cvReleaseImage(&ipl);

return 0;
}
