#include <opencv2/opencv.hpp>

#pragma comment(lib,"comctl32.lib")
#pragma comment(lib,"vfw32.lib")

#define CV_VERSION_STR CVAUX_STR(CV_MAJOR_VERSION) CVAUX_STR(CV_MINOR_VERSION) CVAUX_STR(CV_SUBMINOR_VERSION)

#ifdef _DEBUG
#define CV_EXT_STR "d.lib"
#else
#define CV_EXT_STR ".lib"
#endif

#pragma comment(lib,"opencv_calib3d" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_features2d" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_flann" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_core" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_hal"CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_highgui"CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_imgcodecs"CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_imgproc"CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_ml" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_objdetect" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_photo" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_shape" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_stitching" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_superres" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_ts" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_video" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_videoio" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"opencv_videostab" CV_VERSION_STR CV_EXT_STR)
#pragma comment(lib,"IlmImf"CV_EXT_STR)
#pragma comment(lib,"ippicvmt.lib")
#pragma comment(lib,"libjasper"CV_EXT_STR)
#pragma comment(lib,"libjpeg"CV_EXT_STR)
#pragma comment(lib,"libpng"CV_EXT_STR)
#pragma comment(lib,"libtiff"CV_EXT_STR)
#pragma comment(lib,"libwebp"CV_EXT_STR)
#pragma comment(lib,"zlib"CV_EXT_STR)
