//http://image.onishi-lab.jp/002.html#2
#include <stdio.h>
#include <stdlib.h>

int ppm_read(char *filename, unsigned char *pimage); //上と同じ
int pgm_write(char *filename, unsigned char *pimage); //上と同じ

//intを二乗する
int i_square(int i){
  return i*i;
}

main(){
  unsigned char *back; //背景
  unsigned char *image; //取り込む画像
  unsigned char *sabun; //領域
  int x,y,diff,no;
  char filename[64];
  FILE *fp;
  
  back  = (unsigned char *) malloc(sizeof(unsigned char)*320*240*3); //メモリの確保
  image = (unsigned char *) malloc(sizeof(unsigned char)*320*240*3);
  sabun = (unsigned char *) malloc(sizeof(unsigned char)*320*240);
  
  ppm_read("image/back.ppm", back); //ファイルの読み込み
  
  for(no=1;no<=1;no++){
    sprintf(filename,"image/0000000%d.ppm",no);
    ppm_read(filename, image); //ファイルの読み込み
    
    for(y=0;y<240;y++){ //単純な差分
      for(x=0;x<320;x++){
        diff = i_square(*(image+3*(320*y+x)+0)-*(back+3*(320*y+x)+0)) +  i_square(*(image+3*(320*y+x)+1)-*(back+3*(320*y+x)+1)) + i_square(*(image+3*(320*y+x)+2)-*(back+3*(320*y+x)+2));
      
        if(diff>400) *(sabun+320*y+x) = 0xff;
        else *(sabun+320*y+x) = 0x00;
      }
    }
    
    sprintf(filename,"image/sabun_%02d.pgm",no);
    pgm_write(filename, sabun); //ファイルの書き込み
  }
  free(image); //メモリの開放
  free(sabun);
  free(back);
}


//ppm ファイルを読み込む関数（画像サイズは320×240のみ対応）
int ppm_read(char *filename, unsigned char *pimage){
  FILE *fp;
  if((fp=fopen(filename,"rb"))==NULL){
     printf("ファイル%sが開けません\n",filename);
     exit(-1);
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
  fprintf(fp,"P5\n320 240\n255\n");
  fwrite(pimage,sizeof(char),320*240,fp);
  fclose(fp);
  return 0;
}
