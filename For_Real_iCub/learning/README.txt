//////////////////////////////////////
real iCub data�p�v���O�����Q�Ɋւ���README
learning program
Akira Taniguchi 2016/08/21(for simulator)->2016/11/30(�ύX�E�Ή��t�����m�F)
//////////////////////////////////////

[folder]
/data/
�e�X�g���s�p�̊w�K�f�[�^��ۑ����Ă����B
���݂͕s�g�p�B

/sankou/
�v���O�����쐬���ɎQ�l�ɂ������v���O����

/torioki/
�w�K�p�v���O�����̕ʃo�[�W�����i��r�p�̕ʎ�@�j��ۑ�

[file]

__init__.py�F�w�K�p�̃p�����[�^�̏����l��ݒ肷��t�@�C��
action.py�F�A�N�V���������p�v���O�����i�w�K�ς݃t�@�C���ƒP��f�[�^����s���𐶐�����j
actiondatacollector.py�Flearn.py�����s����O�ɁAiCub_SIM��daump�t�@�C������A�N�V�����f�[�^���w�K�p�f�[�^�Ƃ��Ē��o����v���O�����B
ARI.py�F�w�K���ꂽ�f�[�^�̗v�f���Ƃ̃J�e�S�����ʂƐ^�́i�l�Ԃ́j�J�e�S�����ʂ�ARI���v�Z����
ARI_Fd.py:
ARI_attention.py�FAttention�������݂̂̂Ɋւ���ARI���v�Z����
CNN_feature.py�F���̉摜�t�@�C������CNN�����ʂ����o���v���O����
CNNPCA_action.py�F�A�N�V���������^�X�N�p��CNN-PCA�����𒊏o����v���O����
dsift.py�FDSIFT�𒊏o����v���O����
learn.py�F�w�K�p�v���O�����B�M�u�X�T���v�����O�����s����B
meanARI.py�F�e���s���Ƃ�ARI��ǂݍ��݁A���ϒl���o��
mearnARI_attention.py�FAttention ���݂̂̂�ARI�̕��ς��o��
PCA.py�FCNN������PCA�Œ᎟��������i�g�p���Ă���sklearn.decomposition�̓s����A�w�肵����������菭�Ȃ��������ɂȂ�ꍇ������j
PCA_rename.py:(�f�[�^�����ƂɃt�@�C�������قȂ�o�[�W����)
plot_gmm.py�F�ʒu�J�e�S���̃K�E�X���z���v���b�g����v���O����
sift.py�FSIFT��RGB�����𒊏o����
sift_action.py�F�A�N�V���������^�X�N�pSIFT���o���Ak-means��BOW�𓾂�v���O�����i�H�j
sift_read_kmeans.py�F�摜����SIFT��k-means����BOW�𓾂�u���O�����i�H�j

actionSelectObject_real.py : ���̑I�������̂��߂̃v���O����


[�������s�菇]
1.datadump�t�H���_�Ƀf�[�^��p�ӂ���
2.__init__.py�t�@�C���̃p�����[�^��ݒ肷��
3.�摜�����𒊏o����B�iCNN_feature.py and sift_rename.py�j
4.CNN4096�����f�[�^�̏ꍇ�APCA�Œ᎟��������B�iPCA_rename.py�j
5.����f�[�^�̕ϊ��������s���B�iactiondatacollector.py�j
6.�P��f�[�^��p�ӂ���B���s�R�[�h��Linux�p��LF�݂̂ɂ��Ă������ƁB�its_words.csv�j
6.�w�K�ilearn.py�j

[���̑I��(actionSelectObject_real.py)]
python ./learning/action_real.py $folder $bun $trial $action
folder="ts"
bun="${folder}(${sn}-${en})"
trial="cnnpca006"
