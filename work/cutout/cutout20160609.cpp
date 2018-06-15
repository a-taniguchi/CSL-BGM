//Akira Taniguchi 2016/06/08
//back.cpp::http://image.onishi-lab.jp/002.html#2
//OpenCVlabeling.cpp::http://qiita.com/wakaba130/items/9d921b8b3eb812e4f197
//henkan.cpp::http://opencv.jp/cookbook/opencv_img.html
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <opencv/cv.h>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include "./opencv_lib.hpp"
//#include <time.h>
#include <unistd.h>

int ppm_read(char *filename, unsigned char *pimage); //上と同じ
int pgm_write(char *filename, unsigned char *pimage); //上と同じ

//intを二乗する
int i_square(int i){
  return i*i;
}

//実行は、「./cutout filename」のようにコマンド引数をつける
int main(int argc, char *argv[]){
  int i,j,x,y,diff,no;
  char filename[64];
  char trialname[64];
  FILE *fp;
  unsigned char *back; //背景
  unsigned char *image; //取り込む画像
  unsigned char *sabun; //領域
  
  back  = (unsigned char *) malloc(sizeof(unsigned char)*320*240*3); //メモリの確保
  image = (unsigned char *) malloc(sizeof(unsigned char)*320*240*3);
  sabun = (unsigned char *) malloc(sizeof(unsigned char)*320*240*1);
  
  //no = atoi(argv[1]);
  sprintf(trialname,argv[1]);// = argv[1];
  printf("%s\n",trialname);
  ppm_read("/home/akira/Dropbox/iCub/datadump/initial/leftcam.ppm", back); //背景ファイルの読み込み

  //sprintf(filename,"~/Dropbox/iCub/datadump/%05d",no);//
  //_mkdir(filename);//ファイルは別で作成
  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/object_center.txt",trialname);//
  fp = fopen(filename, "w");

  //for(no=1;no<=1;no++){
  no = 1; //kari  
  i = 0;
  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/cam/left/00000005.ppm",trialname);
  printf("read:%s\n",filename);  
  no = ppm_read(filename, image); //ファイルの読み込み
  while (no == 1){
  	  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/cam/left/0000000%d.ppm",trialname,i);
      no = ppm_read(filename, image); //ファイルの読み込み
      i++;
  }
  printf("read ok!\n");
  ////////////////////背景差分処理////////////////////
  for(y=0;y<240;y++){ //単純な差分
    for(x=0;x<320;x++){
      diff = i_square(*(image+3*(320*y+x)+0)-*(back+3*(320*y+x)+0)) +  i_square(*(image+3*(320*y+x)+1)-*(back+3*(320*y+x)+1)) + i_square(*(image+3*(320*y+x)+2)-*(back+3*(320*y+x)+2));
      
      if(diff>400) *(sabun+320*y+x) = 0xff;
      else *(sabun+320*y+x) = 0x00;
    }
  }
  sprintf(trialname,argv[1]);// = argv[1];
  printf("sabun syori ok!\n");
  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/image/sabun.pgm",trialname);
  printf("write:%s\n",filename);  
  pgm_write(filename, sabun); //ファイルの書き込み
  ////////////////////背景差分処理////////////////////
  printf("haikei sabunn kanryo.\n");
  ////////////////////ラベリング処理////////////////////
  
  //グレースケール入力
  cv::Mat src = cv::imread(filename, cv::IMREAD_GRAYSCALE);
  
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
  cv::Mat Obj0(src.size(), CV_8UC3); //dummy
  cv::Mat Obj1(src.size(), CV_8UC3);
  cv::Mat Obj2(src.size(), CV_8UC3);
  cv::Mat Obj3(src.size(), CV_8UC3);
  cv::Mat Obj4(src.size(), CV_8UC3);
  cv::Mat Obj[5] = {Obj0,Obj1,Obj2,Obj3,Obj4};
  float objx[4];
  float objy[4];
  
  for (int i = 1; i < Dst.rows; ++i) {
    int *lb = LabelImg.ptr<int>(i);
    cv::Vec3b *pix = Dst.ptr<cv::Vec3b>(i);
    for (int j = 0; j < Dst.cols; ++j) {
      pix[j] = colors[lb[j]];
    }
  }
  printf("%d\n",nLab);
  int object_num = 0;
  //ROIの設定
  for (int i = 1; i < nLab; ++i) {
    int *param = stats.ptr<int>(i);
    
    int x = stats.at<int>(i,cv::CC_STAT_LEFT);
    int y = stats.at<int>(i,cv::CC_STAT_TOP);
    int w = stats.at<int>(i,cv::CC_STAT_WIDTH);
    int h = stats.at<int>(i,cv::CC_STAT_HEIGHT);
    int area = stats.at<int>(i,cv::CC_STAT_AREA);
    if(area >= 500 && 5000 >= area && object_num < 4 && 0 <= x && x <= 320 && 0 <= y && y <= 240 && 0 <= w && w <= 320 && 0 <= h && h <= 240){
      
      //int x = param[cv::ConnectedComponentsTypes::CC_STAT_LEFT];
      //int y = param[cv::ConnectedComponentsTypes::CC_STAT_TOP];
      //int height = param[cv::ConnectedComponentsTypes::CC_STAT_HEIGHT];
      //int width = param[cv::ConnectedComponentsTypes::CC_STAT_WIDTH];
      
      cv::rectangle(Dst, cv::Rect(x, y, w, h), cv::Scalar(255, 255, 255), 1);
      //}
      
      //重心の出力
      //for (int i = 1; i < nLab; ++i) {
      //double *param = centroids.ptr<double>(i);
      float x2 = static_cast<float>(x);
      float y2 = static_cast<float>(y);
      float w2 = static_cast<float>(w);
      float h2 = static_cast<float>(h);
      

      cv::circle(Dst,cv::Point(x2 + w2/2, y2 + h2/2), 2, cv::Scalar(0, 0, 255), -1);
      
      //物体ごとの重心を描画
      cv::circle(Obj[object_num],cv::Point(x2 + w2/2, y2 + h2/2), 2, cv::Scalar(255, 255, 255), -1);
      objx[object_num] = x2 + w2/2;
      objy[object_num] = y2 + h2/2;

      
      //}
      
      //面積値の出力
      //for (int i = 1; i < nLab; ++i) {
      //int *param = stats.ptr<int>(i);
      std::cout << "area "<< object_num+1 <<" : " << area << std::endl;
      object_num++;
      
      //ROIの左上に番号を書き込む
      //int x = param[cv::ConnectedComponentsTypes::CC_STAT_LEFT];
      //int y = param[cv::ConnectedComponentsTypes::CC_STAT_TOP];
      std::stringstream num;
      num << object_num;
      cv::putText(Dst, num.str(), cv::Point(x+5, y+20), cv::FONT_HERSHEY_COMPLEX, 0.5, cv::Scalar(255, 255, 255), 1);
    }
  }
  
  //cv::imshow("Src", src);
  //cv::imshow("Labels", Dst);
  sprintf(trialname,argv[1]);// = argv[1];
  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/image/label.ppm",trialname);//
  printf("write:%s\n",filename);
  //ppm_write(filename, Dst);
  //imwrite(const string& filename, const Mat& img, const vector<int>& params=vector<int>()
  imwrite(filename, Dst);

  std::cout << "object num: " << object_num << std::endl;
  fprintf(fp,"%d\n",object_num);
  
  for (int i = 0;i< object_num;i++){
    if(i >= 4){
      printf("over object num.\n");
    }
    else{
      ////////////////////物体領域切り出し処理////////////////////
      //イメージをロード
      sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/cam/left/00000005.ppm",trialname);
      printf("read:%s\n",filename);
      IplImage* ipl = ::cvLoadImage(filename, CV_LOAD_IMAGE_ANYDEPTH | CV_LOAD_IMAGE_ANYCOLOR);
      
      j = 0;
      if(ipl == 0){
      	  sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/cam/left/0000000%d.ppm",trialname,j);
          printf("read:%s\n",filename);
          IplImage* ipl = ::cvLoadImage(filename, CV_LOAD_IMAGE_ANYDEPTH | CV_LOAD_IMAGE_ANYCOLOR);
          j++;
      }
      
      //64x64でROIを設定
      ::cvSetImageROI(ipl, ::cvRect(objx[i]-32, objy[i]-32, 64, 64));
      
      
      //ROIを設定した状態でセーブ
      sprintf(trialname,argv[1]);// = argv[1];
      sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/image/object_%02d.ppm",trialname,i+1);//
      printf("write:%s\n",filename);
      ::cvSaveImage(filename, ipl);
      
      //ROIの解除
      ::cvResetImageROI(ipl);
      
      //イメージの解放
      ::cvReleaseImage(&ipl);
      ////////////////////物体領域切り出し処理////////////////////
      
	  
      //sprintf(filename,"./image/obj_point_%02d_%02d.ppm",no,i);//
      //imwrite(filename, Obj[i]);
      
      ////////////////////透視変換処理処理////////////////////
      //sprintf(filename,"./image/obj_point_%02d_%02d.ppm",no,i);//
      //sprintf(filename,"./image/00000001.ppm");//test
      cv::Mat src_img = Obj[i];//cv::imread(filename, 1);
      if(src_img.empty()) return -1;
      //左上、左下、右下、右上（ｘ，ｙ）
      cv::Point2f pts1[] = {cv::Point2f(68,51),cv::Point2f(-60,260),cv::Point2f(444,260),cv::Point2f(276,51)};
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
      
      //cv::namedWindow("src", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
      //cv::namedWindow("dst", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
      //cv::imshow("src", src_img);
      //cv::imshow("dst", dst_img);
      
      sprintf(filename,"/home/akira/Dropbox/iCub/datadump/%s/image/henkan_%02d.pgm",trialname,i+1);//
      //sprintf(filename,"./image/henkan.ppm");//test
      cv::imwrite(filename,dst_img);
      //cv::imwrite(filename,dst_img);
      
      ////////////////////透視変換処理処理////////////////////
      //一度ファイルにはいて読み込まないとエラーが出る
      ////////////////////再ラベリング処理////////////////////
      //グレースケール入力
      cv::Mat src2 = cv::imread(filename, cv::IMREAD_GRAYSCALE);
      
      //ラべリング処理
      cv::Mat LabelImg2;
      cv::Mat stats2;
      cv::Mat centroids2;
      //int nLab = cv::connectedComponentsWithStats(src, LabelImg, stats, centroids);
      int nLab2 = cv::connectedComponentsWithStats(src2, LabelImg2, stats2, centroids2);
      //printf("%d\n",nLab2);
      //if (nLab2 != 1){
      //printf("henkan or labeling error.\n");
      //}
      //else{
	  //i = 1;
      //int *param = stats2.ptr<int>(1);
      
      int x = stats2.at<int>(1,cv::CC_STAT_LEFT);
      int y = stats2.at<int>(1,cv::CC_STAT_TOP);
      int w = stats2.at<int>(1,cv::CC_STAT_WIDTH);
      int h = stats2.at<int>(1,cv::CC_STAT_HEIGHT);
      //int area = stats.at<int>(i,cv::CC_STAT_AREA);

      float x2 = static_cast<float>(x);
      float y2 = static_cast<float>(y);
      float w2 = static_cast<float>(w);
      float h2 = static_cast<float>(h);

      objx[i] = x2 + w2/2;
      objy[i] = y2 + h2/2;
      printf("ojbect center %d : (%f,%f)\n",i+1,objx[i],objy[i]);
      if(0 <= x && x <= 200 && 0 <= y && y <= 200 && 0 <= objx[i] && objx[i] <= 200 && 0 <= objy[i] && objy[i] <= 200){
         fprintf(fp,"%d, %f,%f\n",i+1,objx[i],objy[i]);
	  }
	  else{
	     printf("object position error.\n");
	     fprintf(fp,"%d, 0,0\n",i+1);
	  }
	  //}
      ////////////////////再ラベリング処理////////////////////
      
    }
  }

  fclose(fp);

 
  ////////////////////ラベリング処理////////////////////
 
  
  cv::waitKey();
  
  //}
  
  free(image); //メモリの開放
  free(sabun);
  free(back);
}




//ppm ファイルを読み込む関数（画像サイズは320×240のみ対応）
int ppm_read(char *filename, unsigned char *pimage){
  FILE *fp;
  int i=0;
  while( (fp=fopen(filename,"rb"))==NULL ){
     printf("ファイル%sが開けません\n",filename);
     sleep(1); /* 秒単位。1秒待つ */     
     i++;
     //exit(-1);
     if(i >= 10){
       return 1;
     }
  }
  fscanf(fp,"P6\n320 240\n255\n"); //ヘッダを読み飛ばす
  fread(pimage,sizeof(char),320*240*3,fp);
  fclose(fp);
  return 0;
}

//pgm ファイルを書き込む関数（画像サイズは320×240のみ対応）
int pgm_write(char *filename, unsigned char *pimage){
  FILE *fp;
  fp=fopen(filename,"wb");
  //printf("a\n");
  fprintf(fp,"P5\n320 240\n255\n");
  //printf("c\n");
  fwrite(pimage,sizeof(unsigned char),320*240,fp);
  //printf("b\n");
  fclose(fp);
  return 0;
}
