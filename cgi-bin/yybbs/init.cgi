#��������������������������������������������������������������������
#�� YY-BOARD v6.21
#�� init.cgi - 2007/09/18
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� 
#�� �\�\�\�\�\�\�\�\�\�\�\�\�\�\[���ӎ���]�\�\�\�\�\�\�\�\�\�\�\�\�\�\
#�� 
#�� �{�X�N���v�g�ɂ��āAKENT WEB�T�|�[�g�f���ւ̎���͋֎~�ł��B
#�� ���p�K������Ȃ��ꍇ�ɂ͖{�����X�N���v�g�̎g�p����ؔF�߂܂���B
#�� 
#�� �\�\�\�\�\�\�\�\�\�\�\�\�\�\[���ӎ���]�\�\�\�\�\�\�\�\�\�\�\�\�\�\
#�� 
#�� 
#�� Antispam Version Modified by isso.
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������
$ver = 'YY-BOARD v6.21 Rev2.52';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. ���ϔ�CGI�ݒu�Ɋւ��邲����͐ݒuURL�𖾋L�̂����A���L�܂ł��肢���܂��B
#��    http://swanbay-web.hp.infoseek.co.jp/index.html
#��    ���₢���킹�O�ɁA�u���̃T�C�g�ɂ��āv
#��    http://swanbay-web.hp.infoseek.co.jp/about.html
#��    �u�悭���邲����v
#��    http://swanbay-web.hp.infoseek.co.jp/faq.html
#��   �u���₢���킹�Ɋւ��钍�ӎ����v
#��    http://swanbay-web.hp.infoseek.co.jp/mail.html
#��    �ɕK���ڂ�ʂ��Ă��������B
#��
#��    �ŐV��NG���[�h�f�[�^�t�@�C���͉��L���_�E�����[�h���Ă��������B
#��    http://swanbay-web.hp.infoseek.co.jp/spamdata.shtml
#��
#��    �f���ւ̃����N���@��Javascript�\��������@�͉��L���Q�Ɖ������B
#��    http://swanbay-web.hp.infoseek.co.jp/cgi-bin/javascript.html
#��
#��    �A�N�Z�X����IP�A�h���X�t�@�C�����L���_�E�����[�h���Ă��������B
#��    �ʏ�A���̃A�N�Z�X����IP�t�@�C���𗘗p����͕K�v����܂���B
#��    ���̃t�@�C���𗘗p�������Ƃɂ�邢���Ȃ鑹�Q�ɑ΂��Ă������͈�؂̐ӔC�𕉂��܂���B
#��    http://swanbay-web.hp.infoseek.co.jp/accessdeny.html
#���Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
#���{�����X�N���v�g�Ɋւ��Ă�KENT���ɖ₢���킹���Ȃ��悤���肢���܂��B
#���P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
#�� 3. �Y�t�� home.gif �� L.O.V.E �� mayuRin ����ɂ��摜�ł��B
#��������������������������������������������������������������������
#
# �y�t�@�C���\����z
#
#  public_html (�z�[���f�B���N�g��)
#      |
#      +-- yybbs / yybbs.cgi
#            |     regist.cgi
#            |     admin.cgi
#            |     read.cgi
#            |     registkey.cgi
#            |     init.cgi
#            |
#            +-- lib / jcode.pl
#            |         form.pl
#            |         registkey.pl
#            |         list_log_thread.pl
#            |         list_log_tree.pl
#            |         list_log_topic.pl
#            |         check.pl
#            |         howto.pl
#            |         search.pl
#            |         pastlog.pl
#            |         message.pl
#            |         newsort.pl
#            |         pickup.pl
#            |         keitai.pl   ...�g�їp
#            |         webmail.pl  ...WebMail�p
#            |         mimew.pl    ...WebMail�p
#            |
#            +-- data / log.cgi      ...���O�t�@�C��
#            |          count.dat    ...�J�E���^�[�t�@�C��
#            |          pastno.dat   ...�ߋ����O�p
#            |          cmode.dat    ...�J���[���[�h�f�[�^�t�@�C��
#            |          color.dat    ...�J���[�f�[�^�t�@�C��
#            |          init.dat     ...�J���[�f�[�^�����ݒ�t�@�C��
#            |          spamdata.cgi ...NG���[�h
#            |          spamlog.cgi  ...���ۃ��O
#            |          denyaddress.cgi ...�A�N�Z�X�֎~�f�[�^�t�@�C��
#            |
#            +-- img / home.gif, bear.gif, ...
#            |
#            +-- past / 0001.cgi ...
#            |
#            +-- mailchk / ...WebMail�p

#-------------------------------------------------
# ���ݒ荀��
#-------------------------------------------------

# �^�C�g����
$title = "BBS";

# �^�C�g�������F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$tCol = "#008080";

# �^�C�g���T�C�Y
$tSize = '24px';

# �{�������t�H���g
$bFace = '"MS UI Gothic", Osaka, "�l�r �o�S�V�b�N"';

# �{�������T�C�Y
$bSize = '13px';

# �ǎ����w�肷��ꍇ�ihttp://����w��j
$backgif = "http://www.tuat.ac.jp/~kyudo/images/yagasuri.gif";

# �w�i�F���w��
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$bgcolor = "#e1f0f0";

# �����F���w��
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$text = "#000000";

# �����N�F���w��
$link  = "#0000ff";	# ���K��
$vlink = "#800080";	# �K���
$alink = "#ff0000";	# �K�⒆

# �����̕\���`��
# thread : �X���b�h�\���i�m�[�}���j
# tree   : �c���[�\��
# topic  : �g�s�b�N�\��
$view_type = 'topic';

# �O���t�@�C��
$jcode  = './lib/jcode.pl';
$formpl = './lib/form.pl';
$regkeypl = './lib/registkey.pl';
$list_log_thread = './lib/list_log_thread.pl';
$list_log_tree   = './lib/list_log_tree.pl';
$list_log_topic  = './lib/list_log_topic.pl';
$checkpl = './lib/check.pl';
$howtopl = './lib/howto.pl';
$searchpl = './lib/search.pl';
$pastlogpl = './lib/pastlog.pl';
$editlogpl = './lib/editlog.pl';
$messagepl = './lib/message.pl';
$newsortpl = './lib/newsort.pl';
$pickuppl = './lib/pickup.pl';

# �J�E���^�t�@�C��
$cntfile = './data/count.dat';

# �{�̃t�@�C��URL
$bbscgi = './yybbs.cgi';

# �X�V�t�@�C��URL
$registcgi = './regist.cgi';

# �Ǘ��t�@�C��
$admincgi = './admin.cgi';

# �L���\���t�@�C��
$readcgi = './read.cgi';

# ���O�t�@�C��
$logfile = './data/log.cgi';

# �߂���URL (index.html�Ȃ�)
$homepage = "../../new_top.shtml";

# �ő�L����
$max = 100;

# �A�C�R���摜�̂���f�B���N�g��
# �� �t���p�X�Ȃ� http:// ����L�q����
# �� �Ō�͕K�� / �ŕ��Ȃ�
$imgurl = "./img";

# �A�C�R�����`
# ���@�㉺�͕K���y�A�ɂ��āA�X�y�[�X�ŋ�؂�
$ico1 = 'bear.gif cat.gif cow.gif dog.gif fox.gif hituji.gif monkey.gif zou.gif mouse.gif panda.gif pig.gif usagi.gif';
$ico2 = '���� �˂� ���� ���� ���� �Ђ� ���� ���� �˂��� �p���_ �Ԃ� ������';

# �Ǘ��Ґ�p�A�C�R���@�\ (0=no 1=yes)
# (�g����) �L�����e���Ɂu�Ǘ��҃A�C�R���v��I�����A�폜�L�[��
#         �u�Ǘ��p�X���[�h�v����͂��ĉ������B
$my_icon = 0;

# �Ǘ��Ґ�p�A�C�R���́u�t�@�C�����v���w��
$my_gif  = 'admin.gif';

# �A�C�R�����[�h (0=no 1=yes)
$iconMode = 0;

# �ԐM�����Ɛe�L�����g�b�v�ֈړ� (0=no 1=yes)
$topsort = 1;

# �^�C�g����GIF�摜���g�p���鎞 (http://����L�q)
$t_img = "";
$t_w = 150;	# �摜�̕� (�s�N�Z��)
$t_h = 50;	#   �V  ���� (�s�N�Z��)

# �~�j�J�E���^�̐ݒu
#  �� 0=no 1=�e�L�X�g 2=�摜
$counter = 1;

# �~�j�J�E���^�̌���
$mini_fig = 6;

# �e�L�X�g�̂Ƃ��F�~�j�J�E���^�̐F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$cntcol = "#dd0000";

# �摜�̂Ƃ��F�摜�f�B���N�g�����w��
#  �� �Ō�͕K�� / �ŕ��Ȃ�
$gif_path = "./img";
$mini_w = 8;		# �摜�̉��T�C�Y
$mini_h = 12;		# �摜�̏c�T�C�Y

# ���[���A�h���X�̓��͕K�{ (0=no 1=yes)
$in_email = 0;

# �L�� [�^�C�g��] ���̒��� (�S�p�������Z)
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$sub_len = 12;

# �L���� [�^�C�g��] ���̐F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$subcol = "#006600";

# �L���\�����̉��n�̐F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$tblcol = "#ffffff";

# ���e�t�H�[���y�у{�^���̕����F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$formCol1 = "#f7fafd";	# ���n�̐F
$formCol2 = "#000000";	# �����̐F

# �ƃA�C�R��
$home_gif = "home.gif";	# �ƃA�C�R���̃t�@�C����
$home_w = 16;		# �摜�̉��T�C�Y
$home_h = 20;		#   �V  �c�T�C�Y

# �C���[�W�Q�Ɖ�ʂ̕\���`��
#  1 : JavaScript�ŕ\��
#  2 : HTML�ŕ\��
$ImageView = 1;

# �C���[�W�Q�Ɖ�ʂ̃T�C�Y (JavaScript�̏ꍇ)
$img_w = 550;	# ����
$img_h = 450;	# ����

# �y�[�W������̋L���\���� (�e�L��)
# �� �ォ�珇�ɁA�X���b�h�\���A�c���[�\���A�g�s�b�N�\���A�V�����\��
$pglog{'thread'} = 5;
$pglog{'tree'}   = 10;
$pglog{'topic'}  = 10;
$pglog{'new'}    = 10;

# ���e������ƃ��[���ʒm���� (sendmail�K�{)
#  0 : �ʒm���Ȃ�
#  1 : �ʒm���邪�A�����̓��e�L���͒ʒm���Ȃ��B
#  2 : ���ׂĒʒm����B
$mailing = 0;

# ���[���A�h���X(���[���ʒm���鎞)
$mailto = 'xxx@xxx.xxx';

# sendmail�p�X�i���[���ʒm���鎞�j
$sendmail = '/usr/lib/sendmail';

# �����F�̐ݒ�
#  ���@�X�y�[�X�ŋ�؂�
$color = '#000000 #800000 #DF0000 #008040 #0000FF #C100C1 #FF80C0 #FF8040 #000080 #808000 #C0C0C0';

# URL�̎��������N (0=no 1=yes)
$autolink = 1;

# �^�O�L���}���I�v�V����
#  �� <!-- �㕔 --> <!-- ���� --> �̑���Ɂu�L���^�O�v��}��
#  �� �L���^�O�ȊO�ɁAMIDI�^�O �� LimeCounter���̃^�O�ɂ��g�p�\
$banner1 = '<!-- �㕔 -->';	# �f���㕔�ɑ}��
$banner2 = '<!-- ���� -->';	# �f�������ɑ}��

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

# �A�N�Z�X�����i���p�X�y�[�X�ŋ�؂�A�A�X�^���X�N�j
#  �� ���ۃz�X�g�����L�q�i�����v�j�y��z*.anonymizer.com
$deny_host = '';
#  �� ����IP�A�h���X���L�q�i�O����v�j�y��z210.12.345.*
$deny_addr = '';

# �P�񓖂�̍ő哊�e�T�C�Y (bytes)
$maxData = 51200;

# �L���̍X�V�� method=POST ���肷��ꍇ�i�Z�L�����e�B�΍�j
#  �� 0=no 1=yes
$postonly = 1;

# ���T�C�g���瓊�e�r�����Ɏw�肷��ꍇ�i�Z�L�����e�B�΍�j
#  �� �f����URL��http://���珑��
$baseUrl = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/';

# ���e�����i�Z�L�����e�B�΍�j
#  0 : ���Ȃ�
#  1 : ����IP�A�h���X����̓��e�Ԋu�𐧌�����
#  2 : �S�Ă̓��e�Ԋu�𐧌�����
$regCtl = 1;

# �������e�Ԋu�i�b���j
#  �� $regCtl �ł̓��e�Ԋu
$wait = 60;

# ���e��̏���
#  �� �f�����g��URL���L�q���Ă����ƁA���e�ナ���[�h���܂�
#  �� �u���E�U���ēǂݍ��݂��Ă���d���e����Ȃ��[�u�B
#  �� Location�w�b�_�̎g�p�\�ȃT�[�o�̂�
$location = '';

# �֎~���[�h
# �� ���e���֎~���郏�[�h���R���}�ŋ�؂�
$no_wd = '';

# ���{��`�F�b�N�i���e�����{�ꂪ�܂܂�Ă��Ȃ���΋��ۂ���j
# 0=No  1=Yes
$jp_wd = 0;

# URL���`�F�b�N
# �� ���e�R�����g���Ɋ܂܂��URL���̍ő�l
$urlnum = 7;

## --- <�ȉ��́u���e�L�[�v�@�\�i�X�p���΍�j���g�p����ꍇ�̐ݒ�ł�> --- ##
#
# ----------------------------------------------------------------
# �u���e�L�[�v�𗘗p���Ă��X�p�����e�����Ⴊ�񍐂���Ă��܂��B
# �{�����X�N���v�g�́u���e�L�[�v�ȊO�œO��I�ȃX�p���΍�ς݂ł��B
# �X�p���΍��ړI�ł́u���e�L�[�v���p�͈�ؕK�v����܂���B
#                                            commented by isso
# ----------------------------------------------------------------
#
# ���e�L�[�̎g�p�i�X�p���΍�j
# �� 0=no 1=yes
$regist_key = 1;

# ���e�L�[��������(JavaScript�L����)
# 0 : �蓮����
# 1 : ��������(����)
$autokey = 1;

# ���e�L�[�摜�����t�@�C���yURL�p�X�z
$registkeycgi = './registkey.cgi';

# ���e�L�[�Í��p�p�X���[�h�i�p�����łW�����j
$pcp_passwd = '009byy61';

# ���e�L�[���e���ԁi���P�ʁj
#   ���e�t�H�[����\�������Ă���A���ۂɑ��M�{�^�����������
#   �܂ł̉\���Ԃ𕪒P�ʂŎw��
$pcp_time = 30;

# ���e�L�[�摜�̑傫���i10�| or 12�|�j
# 10pt �� 10
# 12pt �� 12
$regkey_pt = 10;

# ���e�L�[�摜�̕����F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
# �� $text�ƍ��킹��ƈ�a�����Ȃ��B�ڗ�������ꍇ�� #dd0000 �ȂǁB
$moji_col = '#dd0000';

# ���e�L�[�摜�̔w�i�F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
# �� $bgcolor�ƍ��킹��ƈ�a�����Ȃ�
$back_col = '#e1f0f0';

#---(�ȉ��́u�ߋ����O�v�@�\���g�p����ꍇ�̐ݒ�ł�)---#
#
# �ߋ����O���� (0=no 1=yes)
$pastkey = 1;

# �ߋ����O�pNO�t�@�C��
$nofile = './data/pastno.dat';

# �ߋ����O�̃f�B���N�g��
#  �� �t���p�X�Ȃ� / ����L�q�ihttp://����ł͂Ȃ��j
#  �� �Ō�͕K�� / �ŕ��Ȃ�
$pastdir = './past';

# �ߋ����O�P�t�@�C���̍s��
#  �� ���̍s���𒴂���Ǝ��y�[�W�������������܂�
$pastmax = 650;

# �P�y�[�W������̋L���\���� (�e�L��)
$pastView = 10;

#-------------------------------------------------
#  �ǉ��ݒ荀�� by isso
#-------------------------------------------------


#-------------------------------------------------
# �Ǘ��Ґݒ�
#-------------------------------------------------
#

# �Ǘ��җp�p�X���[�h (�p�����łW�����ȓ�)
$pass = 'junman66';

# ���L�̐ݒ�͊Ǘ��ҍ��̃`�F�b�N������ꍇ�̂ݕK�v�ɉ����ĕύX���ĉ������B
# �Ǘ��ҍ��̃`�F�b�N�@�\�Ɋւ��ẮA�g�������킩����̂ݎg���Ă��������B
# �g�������킩��Ȃ��Ƃ����₢���킹�ɂ͂������v���܂���B
# 
#   0 : �Ǘ��ҍ��̃`�F�b�N�����Ȃ�
#   1 : �Ǘ��ҍ��̃`�F�b�N������
$adminchk = 1;

# �Ǘ��ҍ��̃`�F�b�N������ꍇ�ɂ͉��L���K���ݒ肵�Ă��������B
# 
# ��ʗ��p�҂��g�p�ł��Ȃ����e�Җ�(�g�p���֎~���閼�O)���w��
# ���Ƃ��΁A$a_name�Ŏw�肵���Ǘ��҂̌f���\�������L�����܂�
# �Ǘ��ҍ��̃`�F�b�N�ɂ��g�p�֎~���閼�O��ݒ肵�܂��B
# �u�Ǘ��v�Ɛݒ肷��Ɓu�Ǘ��v���܂ޖ��O��S�ċ֎~�ł��܂��B
# (��) $AdminName = "�Ǘ��l,�Ǘ���";
$AdminName = "�Ǘ�,yuuki,Admin";

# �Ǘ��җp���[�U�[ID�A�Ǘ��ҕ\����ݒ肵�܂��B
# �Ǘ��җp���[�U�[ID�A�Ǘ��җp�}�X�^�p�X���[�h�ŏ������݂����ꍇ�̂݁A
# ���e�Җ����u�Ǘ��҂̌f���\����($a_name)�v�Ōf����ɕ\�����܂��B
# 
# (�g�p��)
# ���Ȃ܂����uwebmaster�v�A�폜�L�[���u0123�v�œ��e���遨���e�Җ��́u�Ǘ��ҁv�ƕϊ�����ĕ\��
# ���Ȃ܂��𒼐ځu�Ǘ��ҁv��u�Ǘ��l�v�Ɠ��͂��ē��e���遨�u�Ǘ��҂𖼏��܂���v�ƃG���[�\��
# �Ǘ��҈ȊO���Ǘ��҂ɂȂ肷�܂����Ƃ�h���܂��B
# 
# �Ǘ��җp���[�U�[ID�ݒ�
# $AdminName�Ŏw�肵�����O�ȊO�̊Ǘ��҂����m�蓾�Ȃ��K���Ȃ��̂ɕύX���ĉ������B
$admin_id = "Shell";

# �Ǘ��Җ��̕\���F
# �w�肵�Ȃ��ꍇ�͒ʏ�̑I��F�ɂȂ�܂��B
$a_color  = "#000000";

# �Ǘ��҂̌f���\����(���ۂɌf���ɕ\�������Ǘ��҂̖��O)
$a_name   = "Seven &quot;the Admin&quot;";

#-------------------------------------------------
# ���e�ݒ�
#-------------------------------------------------
#
# ���e�t�H�[���\��
# ���e�t�H�[�����f���̏㕔�ɕ\�����邩
# ���j���[�Ƀ����N�\�����邩��I���ł��܂��B
#  0 : ���e�t�H�[�����\��(���j���[�ɂă����N)
#  1 : ���e�t�H�[����\��(�ʏ�)
$postform = 1;

# ���e�����[�h�ݒ�
# ���e�����[�h�ɂ���ƑS�Ă̓��e�������ɂ��邱�Ƃ��ł��܂��B
# �S�Ă̓��e�͊Ǘ����[�h���瓊�e�������܂Ō��J����܂���B
#  0 : �ʏ퓊�e���[�h�ɂ���
#  1 : ���e�����[�h�ɂ���
$allowmode = 0;

# ���e����
# �o�^���ꂽ�A�h���X����̓��e�́A�������݂��ꂸ�ɋ��ۃ��O�ɋL�^����܂��B
# ���e�����J����ꍇ�ɂ͊Ǘ����[�h����X�p�����e���O���{�����ē��e���������ĉ������B
# ���e�����ł�����{��(�A�N�Z�X)�Ɋւ��Ă͐����͂���܂���B
# 
# ���e�����z�X�g�����L�q
# (�����v�A���p�J���}�ŋ�؂�A�A�X�^���X�N��)
# $dhost = '*-osaka.nttpc.ne.jp,*.o-tokyo.nttpc.ne.jp';
$dhost = '';
# ���e����IP�A�h���X���L�q
# (�O����v�A���p�J���}�ŋ�؂�A�A�X�^���X�N��)
# $daddr = '210.12.345.*,203.232.235.*';
$daddr = '';

# ���e�������ɕ\�����郁�b�Z�[�W
$denymsg = '���̃��b�Z�[�W�͊Ǘ��҂ɂ����J���҂��ł��B';

# ���p���F�ύX
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
# �F�w����s���ƁA>�ň��p���ꂽ�����̐F��ύX���܂�
# ���̋@�\���g�p���Ȃ��ꍇ�͉����L�q���Ȃ��ŉ����� ($refcol = '';)
$refcol = '#808080';

# ���p������/���e�������̔䗦
# ���p�����������铊�e���K�����܂�
# ���e�������ɑ΂�����p�������̔䗦�����̐��l�ȏ�̏ꍇ�A"���p�������������܂�"�ƃG���[�\�����܂��B
# ���l���傫���قǈ��p�Ɋւ��鐧�������܂��Ȃ蓊�e���₷���Ȃ�܂��B
# �����l�� 5�`8(�{)�ŁA0�ɐݒ肷��Ƃ��̋@�\�͖����ɂȂ�܂��B
$rrate = 6;

# ���p�`�F�b�N�{�b�N�X�E�ԐM�{�^���ݒ�
# �ԐM�{�^���̉��Ɉ��p�`�F�b�N�{�b�N�X�\�����邩���Ȃ�����I���ł��܂��B
#  0 : �e�L���̂ݕԐM�{�^����\��(�I���W�i���d�l)
#  1 : ���p�`�F�b�N�{�b�N�X�ƕԐM�{�^����S�ĕ\��
$re_box = 1;

#-------------------------------------------------
# �f���\���ݒ�
#-------------------------------------------------
#
# �^�C�g���ꗗ�\������
#  0    : �e�L���^�C�g�����ꗗ�\�����Ȃ�
#  ���l : �ݒ茏���̐e�L���^�C�g�����ꗗ�\������
#
#  (��)   $alltitle = 20;
#  �V��20�^�C�g��(�e�L��)���ꗗ�\�����܂��B
$alltitle = 20;

# �^�C�g���ꗗ�\�������N��
# �^�C�g���ꗗ�\���̃^�C�g�����N���b�N�����Ƃ��ɁA
# �Y���X���b�h�̐e�L�����ŐV�L���̂�����Ƀ����N���邩��ݒ�ł��܂��B
# 0 : �e�L���Ƀ����N
# 1 : �ŐV�L���Ƀ����N
$newtitle = 1;

# �V�����\���̕\����
# �V�����\���̂Ƃ���1�y�[�W�ɕ\������L������ݒ肵�܂��B
$npage = $pglog{'new'};

# �f���\���`���̏����ݒ�
#  thread  : �X���b�h�`��
#  tree    : �c���[�`��
#  topic   : �g�s�b�N�`��
#  new     : �V�����`��
$list_ini = "topic";

# ����X���b�h���̍ő�\���R�����g��
# �R�����g�����ݒ�l��葽���ꍇ
# �ŐV�̐ݒ茏���݂̂�\�����܂��B
# 0�ɂ���ƃR�����g���ȗ��͂����S�ĕ\�����܂��B
$thmax = 0;

# ���e�ҕ����F�B
#  0 : �ʏ�e�L�X�g�F�ɂ���
#  1 : ���b�Z�[�W�����F�Ɠ����ɂ���
$nam_col = 1;

# �L����NEW�}�[�N��t���鎞��
#  24 : ���e����24���Ԉȓ��̏ꍇ��NEW�}�[�N��t����
$new_time = 24;

# NEW�}�[�N�̕\���`��
#  �摜���g�p�\
#  (��) $newmark = '<img src="./img/new.gif">';
$newmark = '<font color="#ff3300">New!</font>';

# URL�����N�̃A���_�[���C���ݒ�
#  0 : �A���_�[���C����\��
#  1 : �A���_�[���C���\��
$underline = 0;

# email���͎��̃A���_�[���C���ݒ�
#  0 : �A���_�[���C����\��
#  1 : �A���_�[���C���\��
$emline = 1;

# URL���������N�̏ȗ��ݒ�
# URL�������Ȃ�\�������ɍL����ꍇ�A
# �ݒ蕶�����ȏ���ȗ����ĕ\�����܂��B
$max_leng = 80;

# �f���L������
# �f�����ݒ�l(����)�ȏ㗘�p����Ȃ��ꍇ�A
# �f���������I�ɕ����܂��B�����ݒ��180���B
# 0�ɐݒ肷��Ƃ��̋@�\�͖����ɂȂ�܂��B
# �����I�������f���͊Ǘ���ʂ��烏���N���b�N�ōĊJ�ł��܂��B
$clday = 90;

#-------------------------------------------------
# �G���[���O�ݒ�
#-------------------------------------------------
# 
# �G���[���O�L�^�ݒ�
# ����z�X�g����̃G���[���O���L�^���鎞�ԊԊu
# ����z�X�g���瑱���ăG���[���e�������Ă�
# �ݒ莞�ԓ��ł���΋L�^���܂���B(��������΍�)
# �����ݒ��30(�b)�ŁA0�ɐݒ肷��ƃG���[���O���L�^���܂���B
#  0 : �G���[���O���L�^���Ȃ�
$errtime = 3;

# �G���[���O�L�^�ݒ�
# �L�^����G���[�̎�ނ�ݒ肵�܂��B
# �u�S�ẴG���[���L�^�v�ɐݒ肵�Ă�
# Internal Server Error�͋L�^����܂���B
#  0 : ���b�Z�[�W������ꍇ�̂݋L�^����y�����z
#  1 : �S�ẴG���[���L�^����
$errdata = 0;

# �G���[���O�����ݒ�
# �G���[���O�̋L�^�ő匏���A�ݒ�ő匏���𒴂����
# �Â��G���[���珇�Ɏ����폜����܂��B�����l��100���B
$errlog_max = 100;

# �G���[���O�t�@�C��
$er_log = './data/error.cgi';

#-------------------------------------------------
# �J���[���[�h�ݒ�
#-------------------------------------------------
#
# �f���\���`��
# �\�����[�h��YY-BOARD�I���W�i���`���ɖ߂��ꍇ�ɂ͊Ǘ���ʂōs���ĉ������B
# �\�����[�h��V�\���`���ݒ莞�ɂ͊Ǘ���ʂŃJ���[���[�h��I�����Ă��������B

# �J���[���[�h�f�[�^�t�@�C��
$colorfile = './data/cmode.dat';

# �J���[�f�[�^�t�@�C��
$colordata = './data/color.dat';

# �J���[�f�[�^�����ݒ�t�@�C��
$colorinit = './data/init.dat';

# �c���[�\���̑I���L���w�i�F
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$tree_bc = '#ffffa0';

# ���b�Z�[�W�s�Ԋu�ݒ�
# �\�����[�h��YY-BOARD�I���W�i���`���̂Ƃ��ɗL��
# �\�����[�h�ύX���ɂ͊Ǘ����(�J���[���[�h)�Őݒ�
$lheight = "1.3em";

#-------------------------------------------------
# �ݒ�ύX�s�v
#-------------------------------------------------
$border = 1;
$cellspacing = 1;
$cellpadding = 5;
$margin_left = "22px";
$tbl_col0 = $tblcol;
$tbl_col1 = $tblcol;
$topmark = "";
$comark  = "";
$margin_right = "0px";
$width = "90%";

# �@��ˑ������g�p���̃G���[���b�Z�[�W
$pdcerror = "�@��ˑ������͕����������邽�߂����p�ɂȂ�܂���B";

# �@��ˑ������̋����\��
$pdch = "<b style='color:#FF0000;background-color:#FFFF00'>";
$pdcf = "</b>";

# �f���̗��p�`���������t�`���̏ꍇ
# ���ʂ̓��̓t�H�[����}���ł��܂��B
# 
# (��)
# $inputform = <<TEXT;
# ------------------------------------
# ���[�J�[:
# �^��:
# �N��:
# ------------------------------------
# TEXT
$inputform = <<TEXT;
TEXT

# �\���w�b�_(�f���㕔�^�C�g����)�̓��e�ݒ�(�^�O���p�\)
$header = <<HEAD;
<!--��������-->


<!--�����Ɍf���ŏ㕔�ɕ\��������e���L�q���܂�-->


<!--�����܂�-->
HEAD

# �\���t�b�^(�f���ŉ���)�̓��e�ݒ�(�^�O���p�\)
$footer = <<FOOT;
<!--��������-->


<!--�����Ɍf���ŉ����ɕ\��������e���L�q���܂�-->


<!--�����܂�-->
FOOT

#-------------------------------------------------
# ���[���A�h���X���͐ݒ�
#-------------------------------------------------
#
# WebMail�@�\�𗘗p����ƁA���e�҂����[���A�h���X�����J���邱�ƂȂ�
# �f���K��҂���̃��[�����󂯎�邱�Ƃ��ł��܂�(sendmail�K�{)�B
# 
# WebMail�̗��p
#  0 : ���p���Ȃ�
#  1 : ���p���� (sendmail�K�{�ł�)
$webmail = 0;

# ���{��`�F�b�N
# ���[���̃��b�Z�[�W���ɓ��{�ꂪ����ꍇ�̂�
# ���M���������邱�Ƃ��ł��܂��B
# 0 : ���{����܂܂Ȃ����[���̑��M��������
# 1 : ���{����܂܂Ȃ����[���̑��M�͋��ۂ���
$japanese = 1;

# ���[���A�h���X�̉ߋ����O�ł̕\��
# ���[���A�h���X���ߋ����O�ŕ\�����邩�ǂ�����ݒ肵�܂��B
#  0 : �\�����Ȃ�
#  1 : �\������
$pastmail = 0;

$usewebmail = "����J" ;
if ( $webmail ) { $usewebmail = "����J(WebMail���p)" ; }

if ($in_email) { $mailopt = "���J" } else { $mailopt = "���J�܂��͖��L��";}

# [ �ύX�s�v ] WebMail���C�u����
$webmailpl = './lib/webmail.pl';

# [ �ύX�s�v ] Webmail�F�ؗp�f�B���N�g��
$mailchk = "./mailchk/";

# [ �ύX�s�v ] Webmail���M���O�t�@�C��
$sendmaillog = 'sendmaillog.cgi';

# [ �ύX�s�v ] MIME�G���R�[�h
$mimewpl = './lib/mimew.pl';

#-------------------------------------------------
# �g�їp�ݒ�
#-------------------------------------------------
# 
# �g�т���̉{���Ⓤ�e�A�Ǘ����[�h�ɂ��폜�ɑΉ����Ă��܂����A
# �S�Ă̌g�тł̓����ۏ؂��Ă���킯�ł͂���܂���B

# �g�т̖߂���URL
# �g�т̃g�b�v�y�[�W���ʏ�̃u���E�U�ƈقȂ�ꍇ��
# �g�їp�̃g�b�v�y�[�W��ݒ肵�܂��B
# $khome = "$homepage";�ɐݒ肷��ƃu���E�U�Ɠ����ɂȂ�܂��B
# (�ݒ��) $khome = "http://www.example.com/i/";
$khome = "$homepage";

# �g�їp�X�N���v�g
$kscript = './lib/keitai.pl';

# �g�т�USER_AGENT
@keitai = ('DoCoMo','KDDI','J-PHONE','Vodafone','DDIPOCKET','ASTEL','PDXGW','UP.Browser','MOT-','SoftBank','Mozilla');
@type = ('i','e','j','v','d','a','h','e','v','s','p');

# �g�ѓ��e�F
$kcolor = "#5000B0";

# 1�y�[�W�\���L����
$keitai_page = 10;

# �e�L���̐擪�L��
$treehead = "��";

# �R�����g�擪�L��
$cohead = "�E";

# �X���b�h���R�����g�擪�L��
$thcohead = "��";

# �g�у��[�h�ł�URL�̎��������N
# 0 : ���������N���Ȃ�
# 1 : ���������N����
# �u���������N����v�ɐݒ肷��ꍇ�ɂ́A
# �����N���b�N���\�T�C�g�Ȃǂ�
# �s���T�C�g�ւ̗U�����Ȃ�����������Ď����Ă��������B
$k_link = 0;

# �g�ъǗ����[�h���̕\��
$keitai_mode = "<font color='#ff0000'>�����Ǘ����[�h����</font>";

# Vodafone/J-PHONE��Method=GET�ݒ�
# Vodafone/J-PHONE�œ��e�ł��Ȃ��ꍇ�ɂ�'GET'�ɐݒ肵�܂�
$v_method = 'POST';

$copyright = "- <a href='http://www.kent-web.com/i/'>YY-BOARD</a> -<br>\n".
		"�g�ёΉ� by <a href='http://swanbay-web.hp.infoseek.co.jp/i/'>isso</a>\n";

#-------------------------------------------------
# �X�p�����e(��`���e)���ېݒ�
#-------------------------------------------------
# �ʏ�͐ݒ�ύX�̕K�p�͂���܂���(���ɕb���ݒ�)�B
# ���̂܂܂ŉ^�p���Ē����A���ۂł��Ȃ����e��������
# ���邢�͌돈���������ꍇ�ɂ̂ݐݒ��ύX���ĉ������B
# [��{�ݒ�] �݂̂̐ݒ�łقƂ�ǑS�ẴX�p����r���ł��܂��B
# �ʏ�� [�g���I�v�V����] ���g�p���Ȃ���(�[���ɐݒ肵��)�������B

# �Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
# [��{�ݒ�]  (�[���ɂ͂����A�K���ݒ肵�ĉ�����)
# �P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
# �t�H�[�����e�m�F�p
# �폜����Ɠ��삵�܂���̂Ő�΂ɍ폜���Ȃ��ŉ������B(�ύX�͉�)
# ���p�̉p��������уA���_�[�X�R�A�̂ݐݒ�\�A�󔒂�L���͐ݒ�s�ł��B
# 
# �ύX����ꍇ�͈Ӗ��s���ȕ�����ɂ��邱�Ƃ����E�߂��܂��B
# (��) $bbscheckmode = 'L4g_Ks16_4Nd9c';
$bbscheckmode = 'YY_BOARD';

# �폜����Ɠ��삵�܂���̂Ő�΂ɍ폜���Ȃ��ŉ������B(�ύX�͉�)
# ���p�̉p��������уA���_�[�X�R�A�̂ݐݒ�\�A�󔒂�L���͐ݒ�s�ł��B
# ���ɕK�p���Ȃ���΁A�ύX�����ɏ����ݒ�̂܂܉^�p���Ă��������B
# 
# �ύX����ꍇ�͈Ӗ��s���ȕ����񂩂��邢��
# cancel,clear,delete,reject,reset,erase,annul,effase
# �Ȃǂ̌��(���܂ޕ�����)�ɂ��ĉ������B
# �������A���Őݒ肷��$postvalue�Ƃ͈Ⴄ������ɂ��Ă��������B
# (��) $writevalue = 'k9SL0sv_3rk_wq2';
# (��) $writevalue = 'cancel';
$writevalue = 'cancel';

# �폜����Ɠ��삵�܂���̂Ő�΂ɍ폜���Ȃ��ŉ������B(�ύX�͉�)
# ���p�̉p��������уA���_�[�X�R�A�̂ݐݒ�\�A�󔒂�L���͐ݒ�s�ł��B
# ���ɕK�p���Ȃ���΁A�ύX�����ɏ����ݒ�̂܂܉^�p���Ă��������B
# 
# �ύX����ꍇ�͈Ӗ��s���ȕ����񂩂��邢��
# cancel,clear,delete,reject,reset,erase,annul,effase
# �Ȃǂ̌��(���܂ޕ�����)�ɂ��ĉ������B
# �������A��Őݒ肵��$writevalue�Ƃ͈Ⴄ������ɂ��Ă��������B
# (��) $postvalue = 'x2oMw7fepc_7ge3';
# (��) $postvalue = 'clear';
$postvalue = 'clear';

# �폜����Ɠ��삵�܂���̂Ő�΂ɍ폜���Ȃ��ŉ������B(�ύX�͉�)
# ���p�̉p��������уA���_�[�X�R�A�̂ݐݒ�\�A�󔒂�L���͐ݒ�s�ł��B
# ���ɕK�p���Ȃ���΁A�ύX�����ɏ����ݒ�̂܂܉^�p���Ă��������B
$formcheck = 'formcheck';

# �f���A�N�Z�X����̌o�ߎ���(�b)
# ���e�t�H�[�����g��Ȃ��v���O�������e�΍�ł��B
# ���e�҂��f�����J���ē��e��������܂ł̍ŏ����ԊԊu�ł��B
# �ʏ�͐��b���x�ɐݒ肵�Ă����܂��B
# �����ݒ��5�b�ŁA�[���ɂ���Ƃ��̃`�F�b�N�͍s���܂���B
$mintime = 5;

# ���e�҂��f�����J���ē��e��������܂ł̍Œ����ԊԊu�ł��B
# �ʏ��7200�b(2����)�`90000�b(25����)���x�ɐݒ肵�Ă����܂��B
# �����ݒ��18,000�b(5����)�ŁA�[���ɂ���Ƃ��̃`�F�b�N�͍s���܂���B
$maxtime = 18000;

# �v���r���[��\���̍ŏ�����
# �A�N�Z�X���瓊�e�܂ł̎��ԊԊu���ݒ�b���ȉ��̏ꍇ�A
# ���e���e���v���r���[�\�����A�N���b�N��ɏ������ݏ��������܂��B
# �ʏ�͏����ݒ�̂܂܂Ŗ�肠��܂���B
# ���ۂ���Ȃ��X�p���������Ȃ�悤�ł����璷���ݒ肵�Ă��������B
# �����l15�`60(�b)�A�����ݒ�� 25(�b)�B
$previewmin = 25;

# �v���r���[��\���̍ő厞��
# �A�N�Z�X���瓊�e�܂ł̎��ԊԊu���ݒ�b���ȏ�̏ꍇ�A
# ���e���e���v���r���[�\�����A�N���b�N��ɏ������ݏ��������܂��B
# �ʏ�͏����ݒ�̂܂܂Ŗ�肠��܂���B
# ���ۂ���Ȃ��X�p���������Ȃ�悤�ł�����Z���ݒ肵�Ă��������B
# �����l1000�`10000(�b)�A�����ݒ��5000�b(��80��)�B
$previewmax = 5000;

# �`�F�b�N�f�[�^�̕���������
# 0 : ���������Ȃ�
# 1 : ����������(��͑΍�)
$fcencode = 1;

# �n�b�V���L�[�̕ϊ��ݒ�
# 0 : �n�b�V���L�[�ϊ����Ȃ�
# 1 : �n�b�V���L�[�ϊ�������(�X�p���΍�)
$keychange = 1;

# ��Ǔ_���`
# ��Ǔ_�Ƃ��ĔF�߂�L����ݒ肵�Ă����܂��B
# ���{��`�F�b�N�ł͋�Ǔ_���܂܂Ȃ��Ɠ��{�ꕶ�ł͂Ȃ��Ɣ��f���܂��B
@period = ("�A","�C","�B","�D","�H","�I");

# �Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
# [���e���ۃ��O�ݒ�]  (�X�p�����e�Ƃ��ċ��ۂ��ꂽ�������݂Ɋւ���ݒ�ł�)
# �P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
# �f���X�p���̓��e���ۃ��O
# �������Ԃ̓��O���L�^���A
# �돈�����Ȃ���΁u�L�^���Ȃ��v�ɂ��ĉ������B
# 
# 0 : �L�^���Ȃ�
# 1 : �S�ẴX�p�����e���L�^����
# 2 : ���{��̓��e�݂̂��L�^���A����ȊO��CGI�G���[��Ԃ�
$spamlog = 2;

# ���e���ۃ��O�t�@�C��
$spamlogfile = './data/spamlog.cgi';

# ���e���ۃ��O1�y�[�W������̕\����
# 20�ɐݒ肷��ƁA���ۃ��O�{����1�y�[�W��20���̋��ۃ��O��\�����܂�
$spamlog_page = 20;

# ���e���ۃ��O�t�@�C���ݒ�
# ���e���ۃ��O�̋L�^�ő匏���A�����l��200���B
$spamlog_max = 200;

# ���e���ۃ��O�Ɏc��URL���e��
# �X�p�����e�ɁA���̐ݒ�l�ȏ��URL���������܂�Ă����ꍇ�A
# ���ۃ��O�ɂ̓��b�Z�[�W�{�����ȗ����ċL�^���܂��B
# �����l��20�`50�A�����l��20�B
$maxurl = 20;

# �Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
# [�I�v�V�����ݒ�]  (�K�p������ΐݒ�ύX���ĉ�����)
# �P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
# �z�X�g���̎擾�ł��Ȃ�IP�A�h���X����̃A�N�Z�X����
# �z�X�g�����擾�ł��Ȃ�IP�A�h���X����̃A�N�Z�X�����ۂ���ꍇ�ɂ� 1 �ɂ��܂��B
# �j�t�e�B�A�Ղ��A�C���t�H�V�[�N���𗘗p���Ă���ꍇ��A
# �Ӗ���������Ȃ��ꍇ�ɂɂ� 0 �̂܂܂ɂ��Ă����Ă��������B
#   0 : �A�N�Z�X��������
#   1 : �A�N�Z�X�����ۂ���
$da = 0;

# �X�p���`�F�b�N�ɘa�ݒ�
# �N�b�L�[�f�[�^������ꍇ(��A���e��)�ɂ�
# �X�p���`�F�b�N���ɘa�����e���₷�����܂��B
# 0 : �ʏ�ʂ�X�p���`�F�b�N������
# 1 : �X�p���`�F�b�N���ɘa����y�����z
$cookiecheck = 1;

# URL�d���������ݐݒ�
# URL���ɋL������URL�Ɠ���URL�����b�Z�[�W���ɏ�����Ă���ꍇ
# �X�p�����e�ƌ��Ȃ��������݂����ۂ��܂��B
# ���{��̃A�_���g�E�o��n�E�����N���b�N���\�X�p����
# ���̌X�������������܂��B
# 
# 0 : URL�̏d���������݂�������
# 1 : �V�K���e�̏ꍇ�̂�URL�̏d���������݂����ۂ���y�����z
# 2 : �ԐM�ł�URL�̏d���������݂����ۂ���
$urlcheck = 1;

# ���O�̍ő咷�ݒ�
# 50�ɐݒ肷��ƁA���O�̒�����50�o�C�g(���{���25����)�ȏ�̏ꍇ�ɓ��e�����ۂ��܂��B
# �[���ɂ���Ƃ��̃`�F�b�N�͍s���܂���B�����ݒ��50(�����l30�`50)�B
$namelen = 50;

# ���e���b�Z�[�W�̍Œᕶ����
# ���b�Z�[�W�̖{�����ɒ[�ɒZ�����e���K���ł��܂��B���Ƃ��΁A" 10 "�ɐݒ肵���ꍇ�́A
# ���p������10�����A�S�p������5�����ȉ��̏ꍇ���e�L�����󗝂����ɃG���[���b�Z�[�W��\�����܂��B
$minmsg = 10;

# �֎~���(NG���[�h�AURL)�o�^�t�@�C��
# �������݋֎~����o�^����t�@�C���ł��B
# ���̃t�@�C���ɓo�^���ꂽ���AURL��{����URL���ɏ������ނƓ��e���ۂ���܂��B
# ���̃t�@�C�����폜����ƁA�֎~���̃`�F�b�N�͍s���܂���B
$spamdata = './data/spamdata.cgi';

# �������X�p���`�F�b�N�pIP�A�h���X�t�@�C��
$spamip = './data/spamip.cgi';

# �ŐV�̋֎~���(NG���[�h�AURL)�o�^�t�@�C���͉��L���_�E�����[�h���Ă��������B
# http://swanbay-web.hp.infoseek.co.jp/spamdata.shtml

# �֎~���(NG���[�h�AURL)�`�F�b�N�ݒ�
# 0 : �V�K���e�̏ꍇ�̂݋֎~���(NG���[�h�AURL)�`�F�b�N������
# 1 : �ԐM�ł��֎~���(NG���[�h�AURL)�`�F�b�N������
$spamdatacheck = 1;

# 0 : ���[���A�h���X���͋֎~���`�F�b�N�����Ȃ�
# 1 : ���[���A�h���X�����֎~���`�F�b�N������
$ngmail  = 1;

# 0 : �^�C�g�����͋֎~���`�F�b�N�����Ȃ�
# 1 : �^�C�g�������֎~���`�F�b�N������
$ngtitle = 1;

# �����ł́A������URL�������݂��֎~���邱�Ƃ��ł��܂��B
# URL�̒��ڏ������݂�������ꍇ($comment_url = 0; �ɐݒ�)��
# URL���������߂���x����ݒ肵�܂��B
# 10�ɐݒ肷��ƁAhttp://�`��10�ȏ㏑�����񂾓��e�����ۂ��܂��B
# �[���ɂ���Ƃ��̃`�F�b�N�͍s���܂���B�����ݒ��5(�����l5�`10)�B
$spamurlnum = $urlnum;

# �f���X�p�����e���̏���
# 0 : CGI(�T�[�o�[)�G���[��Ԃ�
# 1 : �����ɉ��L�̃G���[���b�Z�[�W��\��
# ����ȊO�̐��l : ���l�b��ɃG���[�\��
# 3600�ɐݒ肷���3600�b(60��)��ɉ��L�̃G���[���b�Z�[�W��\��
$spamresult = 1;

# �X�p���Ɣ��f���ꂽ�ꍇ�̕\�����b�Z�[�W
# $spammsg = '���e�͐���Ɏ󗝂���܂���';
# �Ɛݒ肷��ƒʏ�̏������݂Ɠ��e���ۂ���ʂł��Ȃ����邱�Ƃ��ł��܂��B
# �X�p���Ǝ҂ɓ��e���ۂ�m���Â炭�Ȃ�܂��B(���{��X�p���������f������)
# $spammsg = '';
# �ƃ��b�Z�[�W��ݒ肵�Ȃ��ꍇ�ɂ�CGI(�T�[�o�[)�G���[��Ԃ���
# �f�����폜���ꂽ���̂悤�ɐU�镑���܂��B
# �����ݒ��
# $spammsg = '���f���e�Ƃ��Đ���ɏ�������܂���';
$spammsg = '���f���e�Ƃ��Đ���ɏ�������܂���';

# �g�т����URL���͋֎~
# 0 : �g�т���̓��e�ł�URL�̋L�ڂ�������
# 1 : �g�т���̓��e�ł�URL�̋L�ڂ��֎~����
$keitaiurl = 1;

# �`�F�b�N�f�[�^��Javascript�\����
# 1�ɐݒ肷���Javascript�\���ɑΉ����Ă��Ȃ�
# �v���O��������̓��e��r�����邱�Ƃ��ł��܂��B
# ���̋@�\�͌g�тɑ΂��Ă͏�ɖ����ƂȂ�܂��B
# 0 : �`�F�b�N�f�[�^��Javascript�\�����Ȃ�
# 1 : �`�F�b�N�f�[�^��Javascript�\��������(�X�p���΍�)
$javascriptpost = 1;

# �f���ւ̒��ڃA�N�Z�X���e����
# �f���֒��ڃA�N�Z�X�����ꍇ�ɓ��e���֎~�����邱�Ƃ��ł��܂��B
# �f�����X�g���쐬���Ď������e������悤�ȃX�p����r���ł��܂����A
# �u�b�N�}�[�N���璼�ڌf���ɃA�N�Z�X�����ꍇ��Z�L�����e�B�\�t�g���g����
# ���t�@���[�𖳌���(�����N�������폜)���Ă���ꍇ�����e�������󂯂܂��B
# ���̓��e������ݒ肵�Ă��g�т���̓��e�͐������O(���e����)����܂��B
# 0 : ���e��������
# 1 : ���ڂ̓��e���֎~����
# 2 : �uInternal Server Error�v��Ԃ�
$referercheck = 1;

# �^�C�g�����̓`�F�b�N
# 0 : �^�C�g�������͂̂Ƃ��́u����v�ɂ���
# 1 : �^�C�g�������͂̂Ƃ��̓G���[�\������
# 2 : ���p�����݂̂̃^�C�g����http://���܂ރ^�C�g���̂Ƃ��̓G���[�\������
$suberror = 0;

# ���b�Z�[�W���̓��{����`�F�b�N
# ���b�Z�[�W���ɂЂ炪�ȁA�J�^�J�i����ы�Ǔ_���܂܂�Ă��邩���`�F�b�N���܂��B
# 0 : ���b�Z�[�W�ɓ��{�ꂪ�܂܂�Ă��Ȃ��Ă����e��������
# 1 : ���b�Z�[�W�ɓ��{�ꂪ�܂܂�Ă��Ȃ��ꍇ�͓��e�����ۂ���
$asciicheck = 0;

# ���b�Z�[�W�������̃`�F�b�N�ݒ�
# 20�ɐݒ肷��ƁAURL�̋L�ڂ�����ꍇ�Ɍ���
# URL�ȊO�̕����������p������20���������A
# �S�p������10���������̏ꍇ�ɓ��e�����ۂ��܂��B
# �[���ɂ���Ƃ��̃`�F�b�N�͍s���܂���B
$characheck = 0;

# ���e�p�̍������t�ݒ�
# �������t�̓��͂�K�{�Ƃ���ꍇ�ɐݒ肵�Ă��������B
# (�������t�ݒ��)
# $aikotoba = '�ق��ق�';
# �������t�𗘗p���Ȃ��ꍇ�ɂ͉��������Ȃ��ł��������B
$aikotoba = '';

# �������t��ݒ肷��ꍇ�A�������t�̃q���g�������Ă��������B
# (��) �������t�ɂ́��������Ђ炪�Ȃŏ����Ă�������
$hint = "�������t���ɂ�$aikotoba�Ə����Ă�������";

# �f���������T�C�g���{�b�g�̌����Ώۂ���O��
# �f���������T�C�g���{�b�g�̌����Ώۂ���O���ꍇ�ɂ� 1 �ɂ��܂��B
#  0 : ������������
#  1 : �����Ώۂ���O��
$norobot = 1;

# �Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
# [�g���I�v�V�����ݒ�] (���p/���ɕK�v���̂���ꍇ�̂ݐݒ肵�ĉ������B)
# �P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
# ���� [�g���I�v�V����] �͊�{�I�ɂ͐ݒ肹���A�S�ă[���̂܂܂����p�������B
# ���̍��ڂ�ݒ肵�Ȃ��Ă��X�p�����e�͔r���ł��܂��B
# �ݒ肵�ăX�p���`�F�b�N������������ƃX�p�����e�͑S�������Ȃ�܂����A
# ����Ɠ����ɁA���e���̐����������ƒʏ�̓��e������܂��B
# 
# 
# [�g���I�v�V����] URL�̒��ڏ������݂��֎~����
# URL(http://�`)�̃��b�Z�[�W���ւ̒��ڏ������݂��֎~���A
# ttp://�`�Ə������񂾂Ƃ������AURL�̏������݂������܂��B
# 0 : URL�̒��ڏ������݂�������
# 1 : URL�̒��ڏ������݂��֎~����(URL���������ޏꍇ�ɂ� ttp://�`�ƋL�q)
$comment_url = 0;

# [�g���I�v�V����] URL�]���E�Z�kURL�̌f�ڋ֎~�ݒ�
# URL�]���T�[�r�X����ђZ�kURL�T�[�r�X�̋^���̂���URL��
# �{����URL���Ɍf�ڂ����ꍇ�A���e���֎~�����邱�Ƃ��ł��܂��B
# (��) http://symy.jp/ http://xrl.us/ http://jpan.jp/
# http://urlsnip.com/ http://tinyurl.com/ http://204.jp/  �Ȃ�
# 
# 0 : ���e��������
# 1 : ���e���֎~����
$shorturl = 0;

# [�g���I�v�V����] �s���ȍ폜�L�[�̋֎~
# �폜�L�[�ɔ��p�X�y�[�X���܂ޏꍇ��A
# �u111111�v�uaaaaa�v�̂悤�Ȉꎚ�̌J��Ԃ����֎~�ł��܂�
# 0 : �s���ȍ폜�L�[���֎~���Ȃ�
# 1 : �s���ȍ폜�L�[���֎~����
$ng_pass = 0;

# [�g���I�v�V����] ���[���A�h���X�̓��͂��֎~�ł��܂�
# 0 : ���[���A�h���X�̓��͂����R�ɂ���
# 1 : ���[���A�h���X�̓��͂��֎~����
# 2 : ���[���A�h���X�̓��͂̓A�b�g�}�[�N��S�p���́u �� �v�Ɍ��肷��
$no_email = 0;
if ($no_email) { $in_email = 0; }

# [�g���I�v�V����] ���e�[��
# 0 : �g�т���̓��e�̓X�p���`�F�b�N�����߂�
# 1 : �g�т���̓��e�ł��Œ���̃X�p���`�F�b�N������
# 2 : �g�т���̓��e�ł��u���E�U�Ɠ��l�ɃX�p���`�F�b�N������
$keitaicheck = 0;

# [�g���I�v�V����] ���eIP�A�h���X�`�F�b�N�ݒ�
# �A�N�Z�XIP�A�h���X�Ɠ��eIP�A�h���X����v���Ȃ��ꍇ�A
# ���e�����ۂ��邱�Ƃ��ł��܂��B
# 0 : IP�A�h���X����v���Ȃ��Ă����e������
# 1 : IP�A�h���X����v���Ȃ��ꍇ�͓��e���ۂ���
$ipcheckmode = 0;

# ���e�����[�h�ݒ�
# (�ݒ�ύX�s�v)
$postmode = '�X�p�����e';
$alreason = '���e���ۗ��R';
if($allowmode) {
	$previewtime = 0;
	$spamresult = 1;
	$spammsg = '����ɏ�������܂����B�Ȃ��A���e�͊Ǘ��҂̋���Ɍ��J����܂��B';
	$postmode = '���J���҂����e';
	$alreason = '���';
}

# �Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
# [�����A�N�Z�X�����ݒ�] (�ʏ�͐ݒ�ύX�̕K�v�͂���܂���) 
# �P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
# [�����A�N�Z�X�����ݒ�] �����t�@�C��
# �f���ɃA�N�Z�X�����Ƃ��ɃT�[�o�[�G���[�ɂȂ�ꍇ�ɂ�
# ��x���̃t�@�C�����폜���邩�A�����Œ��g����̃t�@�C�����㏑���]�����Ă��������B
# �ʏ�͕ύX���Ȃ��ł��������B
$denyfile = './data/denyaddress.cgi';

# [�����A�N�Z�X�����ݒ�] �������ݒ�
# �L�^����IP�A�h���X����ݒ肵�܂��B(�����l50��)
# �A�N�Z�X��������IP�A�h���X���ݒ萔�𒴂���ꍇ��
# �Â��f�[�^���珇�ɍ폜���܂��B
# �ʏ�͕ύX�̕K�v�͂���܂���B
$denynum = 100;

unless (-e $denyfile) {
	if (-e "./denyaddress.cgi") { $denyfile = "./denyaddress.cgi"; }
}

# �A�N�Z�X����IP�A�h���X�t�@�C��(�O������̃X�p�����ۗp)
$deny_addr_file = './data/deny_addr_file.cgi';

# �A�N�Z�X����IP�ǉ�
@denyaddr= split(/\s+/, $deny_addr);
if (-e $deny_addr_file) {
	open(IN, "$deny_addr_file");
	$deny_addr2 = <IN>;
	close(IN);
	@deny_addr2 = split(/\s+/, $deny_addr2);
	push(@denyaddr, @deny_addr2);
}


#-------------------------------------------------
# ���ݒ芮��
#-------------------------------------------------

# �L���\���^�C�v
%list_type = (
	'thread' => '�X���b�h�\��',
	'tree'   => '�c���[�\��',
	'topic'  => '�g�s�b�N�\��',
	'new'    => '�V�����\��',
	'pickup'  => '�֘A�L���\��',
	);

#-------------------------------------------------
#  �g�ы@��`�F�b�N
#-------------------------------------------------
sub agent {
	# �g�ы@��ݒ�
	my $agent = $ENV{'HTTP_USER_AGENT'};
	$method = 'POST'; $keitai = 'p';

	local ($i) = 0;
	foreach (@keitai) {
		if ($agent =~ /^\Q$_\E/i) { $keitai = $type[$i]; last; }
		$i++;
	}

	#  Vodafone/J-PHONE��Method
	if ($keitai eq  'v' || $keitai eq  'j') { $method = $v_method; }

	# �g�у��[�h�e�X�g�p
#	$keitai = 'i';

	# �g�у��[�h
	if (-e "$kscript" && $keitai ne 'p') { require "$kscript"; }
}

#-------------------------------------------------
#  �A�N�Z�X����
#-------------------------------------------------
sub axsCheck {
	# IP&�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	if ($da) {
		if ($host =~ /\d$/) {
			&error("�z�X�g�����s���Ȃ��߃A�N�Z�X�ł��܂���B<br>\n".
			"�����p�l�b�g���[�N�̊Ǘ��҂�DNS�o�^�����肢���Ă��������B");
		}
	}

	# IP�`�F�b�N
	local($flg);
	foreach (@denyaddr) {
		s/\./\\\./g;
		s/\*/\.\*/g;

		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg) {
		&error("�A�N�Z�X��������Ă��܂���B<br>�f���Ǘ��҂܂ł��₢���킹�������B");

	# �z�X�g�`�F�b�N
	} elsif ($host) {

		foreach ( split(/\s+/, $deny_host) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("�A�N�Z�X��������Ă��܂���");
		}
	}
	if ($host eq "") { $host = $addr; }
	if (-e "$denyfile") { &spambot; }
	if ($keitai eq "p") {
		if ($referercheck == 2 && !$ENV{'HTTP_REFERER'}) { &cgi_error; }
	}
}

#-------------------------------------------------
#  �t�H�[���f�R�[�h
#-------------------------------------------------
sub decode {
	my $buf;
	if ($ENV{'REQUEST_METHOD'} eq "$method") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > $maxData) {
			&error("���e�ʂ��傫�����܂�");
		}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag=0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in);
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JIS�R�[�h�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �G�X�P�[�v
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;
		$val =~ s/\t//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$page = $in{'page'};
	$page =~ s/\D//g;
	if ($page < 0) { $page = 0; }
	$mode = $in{'mode'};

	if ($keychange) {
		if ($mode eq "$writevalue" || $mode eq "sendmail") {
			($in{'email'},$in{'url'}) = ($in{'url'},$in{'email'});
			($in{'comment'},$in{'name'}) = ($in{'name'},$in{'comment'});
		}
	}

	# �^�O����
	$in{'name'} =~ s/>/&gt;/g;
	$in{'name'} =~ s/</&lt;/g;
	$in{'name'} =~ s/"/&quot;/g;
	$in{'name'} =~ s/\r//g;
	$in{'name'} =~ s/\n//g;

	$headflag = 0;
}

#-------------------------------------------------
#  �G���[����
#-------------------------------------------------
sub error {
	my ($msg,$spam) = @_;
	# �G���[���O
	if (!$spam) {
		if ($errtime) {
			if ($errdata || $in{'comment'}) {
				&write_spamlog("$msg","error");
			}
		}
	}
	&header if (!$headflag);
	print <<EOM;
<div align="center">
<hr width="400"><h3>ERROR !</h3>
<font color="red">$_[0]</font>
<p>
<hr width="400">
<p>
<form>
<input type="button" value="�O��ʂɖ߂�" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  HTML�w�b�_
#-------------------------------------------------
sub header {
	$headflag=1;

	if ($keitai eq 'p') {
		print "Content-type: text/html\n\n";
		print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-script-type" content="text/javascript">
<meta http-equiv="content-style-type" content="text/css">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="Mon, 1 Jan 1990 01:01:01 GMT">
<meta http-equiv="Expires" content="0">
EOM
	if ($norobot) {
		print qq|<meta name="ROBOTS" content="NOARCHIVE">\n|;
		print qq|<meta name="ROBOTS" content="NOINDEX,NOFOLLOW">\n|;
	}
	print <<EOM;
<style type="text/css">
<!--
body,td,th { font-size:$bSize; font-family:$bFace; }
EOM
	if ( $scroll ) {
		print qq|body { background-attachment: fixed; }\n|;
	}

	if($underline) {
		print qq|a:hover { color: $alink }\n|;
	} else {
		print qq|a:link    { text-decoration:none; }\n|;
		print qq|a:visited { text-decoration:none; }\n|;
		print qq|a:active  { text-decoration:none; }\n|;
		if($emline) {
			print qq|.e { text-decoration: underline; color:$link; }\n|;
		}
	}
	print qq|a:hover { text-decoration:underline; color:$alink; }\n|;

	print <<EOM;
.n { font-family:Verdana,Helvetica,Arial; }
.b {
	background-color:$formCol1;
	color:$formCol2;
	font-family:Verdana,Helvetica,Arial;
	}
.f {
	background-color:$formCol1;
	color:$formCol2;
	font-size: $bSize;
	}
.topdisp {
	display: none;
}
EOM
	if ($boardmode && -s "$colordata") {
	print <<EOM;
.thread {
	border: $thr_brd solid $tbl_col0;
EOM
	if ($thr_bg && $backgif) {
		print qq|\tbackground-image: url("$backgif")\n|;
	} else {
		print qq|\tbackground-color: $bgcolor;\n|;
	}
	print <<EOM;
	color: $text;
	font-size: $bSize;
	font-family: $bFace
}
.form {
	border: $frm_brd solid $frm_solid;
	background-color: $frm_bc;
	color: $frm_tx;
	font-size: $bSize;
	font-family: $face
}
.alltree {
	border: $allt_brd solid $allt_solid;
	background-color: $allt_col;
	color: $text;
	font-size: $bSize;
	font-family: $bFace
}
input, select {
	border: $btn_brd solid $btn_solid;
	background-color: $formCol1;
	color: $formCol2;
	font-size: 100%;
	font-family: $bFace
}
.menu {
	border: $menu_brd solid $menu_solid;
	background-color: $menu_bg;
	color: $menu_chr;
	font-family: $bFace
	font-size: 100%;
	cursor: hand;
}
.post {
	border: $post_brd solid $post_solid;
	background-color: $post_bg;
	color: $post_chr;
	font-family: $bFace
	font-size: 100%;
	cursor: hand;
}
textarea {
	border-top: $tarea_brd solid $btn_solid;
	border-bottom: $tarea_brd solid $btn_solid;
	border-left: $tarea_brd solid $btn_solid;
	border-right: $tarea_brd solid $btn_solid;
	background-color: $formCol1;
	color: $formCol2;
	font-size: 100%;
}
.radio {
	border: $radio_brd solid $bgcolor;
	background-color: $bgcolor;
	color: $text;
	font-size: 100%;
	font-family: $bFace
}
hr { 
	background-color: $tbl_col0;
	color: $tbl_col0;
	border: none;
	height: 1px;
}
.allow {
	border: $frm_brd solid $frm_solid;
	background-color: $frm_bc;
	color: $text;
	font-family: $face
}
EOM
	}
	print <<EOM;
-->
</style>
EOM
	# JavaScript�w�b�_

	print "<script type=\"text/javascript\">\n",
	"<!-- //\n",
	"function address(){\n",
	"user_name=address.arguments[1];\n",
	"document.write(user_name.link(\"&#109;&#97;&#105;&#108;&#116;&#111;&#58\" + address.arguments[0] + \"&#64;\" + address.arguments[2]));\n",
	"}\n";
	print "function fcheck(){\n",
	"document.write(fcheck.arguments[1] + fcheck.arguments[2] + fcheck.arguments[0] + fcheck.arguments[3]);\n}\n";

	if ($ImageView == 1 && $_[0] eq "ImageUp") {
		print "function ImageUp() {\n";
		print "window.open(\"$bbscgi?mode=image\",\"window1\",\"width=$img_w,height=$img_h,scrollbars=1\");\n}\n";
	}

	print "// -->\n</script>\n";

	print "<title>$title</title></head>\n";
	if ($backgif) {
		print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	} else {
		print "<body bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	}

	} else {
		# �g�їp�w�b�_
		print qq|content-type: text/html\n\n|;
		print qq|<html>\n<head>\n|;
		print qq|<meta http-equiv="content-type" content="text/html; charset=shift_jis">\n|;
		print qq|<meta http-equiv="Cache-Control" content="no-cache">\n|;
		print qq|<meta http-equiv="Pragma" content="no-cache">\n|;
		print qq|<title>$title</title>\n</head>\n<body bgcolor="$bgcolor" text="$text">\n|;
	}
}

#-------------------------------------------------
#  ���������N
#-------------------------------------------------
sub auto_link {
	my ($msg) = @_;
	# ttp�u��
	$msg =~ s/([^=^\"]|^)(http:)/$1ttp:/g;
	$msg =~ s/([^=^\"]|^)(ttps?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/$1h$2/g;
	# ����URL�΍�
	my @url = $msg =~ /([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/g;
	my $i = 0;
	my $flg = 0;
	my @part = ();
	my @match = ();
	my @replce = ();
	foreach (@url){
		if ($_ =~ /(https?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/) {
			$match[$i] = $&;
			($part[$i],$flg) = &short_link($&);
			if ($flg) {
				($replce[$i] = $part[$i]) =~ s/http/\t/;
				$msg =~ s/([^=^\"]|^)(\Q$match[$i]\E)/$1<a href=\"$match[$i]\" target=\"_blank\">$replce[$i]<\/a>/;
			} else {
				($replce[$i] = $match[$i]) =~ s/http/\t/;
				$msg =~ s/([^=^\"]|^)(\Q$match[$i]\E)/$1<a href=\"$match[$i]\" target=\"_blank\">$replce[$i]<\/a>/;
			}
			$i++;
		}
	}
	$msg =~ s/\t/http/g;
	return $msg;
}

#-------------------------------------------------
#  �Z�k�����N
#-------------------------------------------------
sub short_link {
	my ($part) = @_;
	my $flg = 0;
	my $match = $part;
	if(length($match) > $max_leng){
		$part = substr($match, 0, abs($max_leng-15));
		$part .= " \.\.\.\.\. ";
		if($match =~ /(.){10}$/) {
			$part .= $&;
		}
		$flg = 1;
	}
	return ($part,$flg);
}

#-------------------------------------------------
#  �N�b�L�[���s
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# ���ەW�������`
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# �ۑ��f�[�^��URL�G���R�[�h
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# �i�[
	print "Set-Cookie: YY_BOARD=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  �N�b�L�[�擾
#-------------------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# �N�b�L�[�擾
	$cook = $ENV{'HTTP_COOKIE'};

	# �Y��ID�����o��
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# �f�[�^��URL�f�R�[�h���ĕ���
	@cook=();
	foreach ( split(/<>/, $cook{'YY_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#-------------------------------------------------
#  crypt�Í�
#-------------------------------------------------
sub encrypt {
	local($inpw) = @_;
	local(@char, $salt, $encrypt);

	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	$encrypt;
}

#-------------------------------------------------
#  crypt�ƍ�
#-------------------------------------------------
sub decrypt {
	local($in, $dec) = @_;

	local($salt) = $dec =~ /^\$1\$(.*)\$/ && $1 || substr($dec, 0, 2);
	if (crypt($in, $salt) eq $dec || crypt($in, '$1$' . $salt) eq $dec) {
		return (1);
	} else {
		return (0);
	}
}

#-------------------------------------------------
#  ���Ԏ擾
#-------------------------------------------------
sub get_time {
	$times = shift;
	if (!$times) { $ENV{'TZ'} = "JST-9"; $times = time; }

	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# �����̃t�H�[�}�b�g
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
			$year+1900,$mon+1,$mday,$week[$wday],$hour,$min,$sec);
}

#-------------------------------------------------
#  ��������
#-------------------------------------------------
sub message {
	local($msg) = @_;

	&header;
	print <<EOM;
<div align="center">
<hr width="400">
<h3>$msg</h3>
<hr width="400">
<p>
EOM
	if($in{'list'} eq "pickup") {
		print qq|<form action="$bbscgi#$in{'num'}">\n|;
	} else {
		print qq|<form action="$bbscgi">\n|;
	}
	print <<EOM;
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="num" value="$in{'num'}">
<input type="submit" value="�f���ɖ߂�" class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �J���[�ݒ�f�[�^�Ǎ�
#-------------------------------------------------
sub read_color {
	open(COL,"$colorfile") || &error("�J���[���[�h�f�[�^�t�@�C�� $colorfile ������܂���B");
	$colormode = <COL>;
	close(COL);

	local $i = 0;
	open(PARA,"$colordata");
	while (<PARA>) {
		($bgcolor,$text,$cntcol,$tCol,$tblcol,$tbl_col0,$thr_brd,$menu_chr,$menu_bg,$menu_solid,$menu_brd,$allt_col,$allt_solid,$allt_brd,$tbl_col1,$tarea_brd,$btn_col,$btx_col,$btn_solid,$btn_brd,$formCol1,$formCol2,$post_chr,$post_bg,$post_solid,$post_brd,$moji_col,$back_col,$radio_brd,$border,$cellspacing,$cellpadding,$topmark,$comark,$margin_left,$margin_right,$subcol,$sub_len,$frm_brd,$frm_bc,$frm_tx,$frm_solid,$refcol,$tree_bc,$scroll,$thr_bg,$lheight,$width) = split(/<>/);
		if (!$width) { $width = "90%"; }
		if ($colormode == $i) { last; }
		$i++;
	}
	close(PARA);
}

#-------------------------------------------------
#  �t�H�[���`�F�b�N�f�[�^������
#-------------------------------------------------
sub encode_bbsmode {
	local($fck) = shift;
	if(!$fck) { $fck = time; }
	if($fcencode) {
		srand;
		local($en) = rand(4); $en++; $en = int($en);
		if ($en%2) { $fck = sprintf("%X", $fck);
		} else { $fck = sprintf("%x", $fck); }
		if ($en == 1)    { $fck =~ tr/[0-9]/[g-p]/; }
		elsif ($en == 2) { $fck =~ tr/[0-9]/[q-z]/; }
		elsif ($en == 3) { $fck =~ tr/[0-9]/[G-P]/; }
		elsif ($en == 4) { $fck =~ tr/[0-9]/[Q-Z]/; }
		$fck = reverse($fck);
	}
	return $fck;
}

#-------------------------------------------------
#  �t�H�[���`�F�b�N�f�[�^����
#-------------------------------------------------
sub decode_bbsmode {
	local($fck) = shift;
	$fck2 = $fck;
	if ($fck =~ /[a-z]/i) {
		$fck = reverse($fck);
		$fck =~ tr/[g-p]/[0-9]/;
		$fck =~ tr/[q-z]/[0-9]/;
		$fck =~ tr/[G-P]/[0-9]/;
		$fck =~ tr/[Q-Z]/[0-9]/;
		$fck = sprintf("%d", hex($fck));
	}
	if($fck < 0) { $fck = $fck2; }
	return $fck;
}

#-------------------------------------------------
#  �A�h���X�Í���
#-------------------------------------------------
sub encode_addr {
	local ($adr,$i);
	$adr = shift;
	if (!$adr) { $adr = $addr; }
	$i = 0;
	foreach (split(/\./, $adr)) {
		$addr[$i] = sprintf("%02x", $_);
		$i++;
	}
	$enadr = substr(crypt(join('',@addr), $addr[0]), 2);
	return $enadr;
}

#-------------------------------------------------
#  �G���e�B�e�B��
#-------------------------------------------------
sub entity {
	my $str = shift;
	my $ent = "";
	for (0 .. length($str)-1) {
		$ent .= "&#".ord(substr($str, $_, 1)).";";
	}
	return $ent;
}

#-------------------------------------------------
#  �G�X�P�[�v
#-------------------------------------------------
sub escape {
	my ($str) = @_;
	$str =~ s/[\x00-\x1F\x7F]//g;
	$str =~ s/&/&amp;/g;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/"/&quot;/g;
	$str =~ s/'/&#x27;/g;
	return $str;
}

#-------------------------------------------------
#  �X�p��/�G���[���O�L�^
#-------------------------------------------------
sub write_spamlog {
	my ($reason,$job) = @_;
	$reason =~ s/\r\n//g;
	$reason =~ s/\r//g;
	$reason =~ s/\n//g;

	if ($job eq "error")  {
		my ($cnam,$ceml,$curl) = &get_cookie;
		if (!$in{'name'})  { $in{'name'}  = $cnam; }
		if (!$in{'email'}) { $in{'email'} = $ceml; }
		if (!$in{'url'})   { $in{'url'}   = $curl; }
		if ($in{'pwd'})    { $ango = &encrypt($in{'pwd'}); }
	}

	my $log_comment = $in{'comment'};
	my $log_name    = $in{'name'};
	my $log_email   = $in{'email'};
	my $log_url     = $in{'url'};
	my $log_sub     = $in{'sub'};
	if (!$log_sub) {
		$log_sub = "����";
	} 
	if (length($log_comment) < length($log_name)) {
		($log_comment,$log_name) = ($log_name,$log_comment);
	}
	if ($job ne "error")  {
		if($spamlog == 2) {
			# �Ђ炪�Ȃ��܂܂Ȃ��X�p���͋L�^���Ȃ�
			if ($log_comment !~ /(\x82[\x9F-\xF2])/) {
				if ($spammsg) { &message("$spammsg"); } else { &cgi_error; }
			}
		}
	}

	if ($log_url =~ /\@/ || $log_email && $log_email !~ /\@/) {
		($log_email,$log_url)=($log_url,$log_email);
	}

	my $num = ($log_comment =~ s/http/http/ig);
	if($num >= $maxurl) { $log_comment ="���b�Z�[�W����URL����$num�Ƒ������߁A���b�Z�[�W�{���폜"; }
	$log_comment =~ s/"/&quot;/g;

	my $times = time;
	my $date = &get_time($times, "log");
	my $log_times = $in{"$bbscheckmode"};
	if (!$log_times) { $log_times = $times; }

	# ���O���`
	my $file = $spamlogfile;
	my $logmax = $spamlog_max;
	if ($job eq "error")  {
		$file = $er_log;
		$logmax = $errlog_max;
	}

	# ���O���J��
	open(IN,"+<$file");
	eval { flock(IN, 1); };
	# �Â��X�p�����O���폜
	my $i = 1;
	my $flg = 0;
	my @new = ();
	while (<IN>) {
		# �A�����e�`�F�b�N
		if ($i == 1) {
			my ($n,$r,$d,$a,$e,$s,$m,$u,$ho,$p,$c,$ic,$tm) = split(/<>/, $top);
			if (abs(time - $tm) < $errtime) {
				if ($host eq $ho) {
					$flg = 1;
				}
			}
		}
		# �Â��X�p�����O���폜
		if ($i < $logmax) {
			push(@new,$_);
		}
		$i++;
	}
	close(IN);

	# �A�����e�ȊO���L�^
	if (!$flg) {
		# �X�p��/�G���[���O���X�V
		my $new = "$no<>$in{'reno'}<>$date<>$log_name<>$log_email<>$log_sub<>$log_comment<>$log_url<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>$reason<>$log_times<>$ENV{'HTTP_REFERER'}<>$ENV{'HTTP_USER_AGENT'}<>$times<>\n";
		unshift (@new,$new);
		open(OUT,"+>$file");
		eval { flock(OUT, 2); };
		seek(OUT, 0, 0);
		print OUT @new;
		close(OUT);
	}
}

#-------------------------------------------------
#  �A�N�Z�X�����`�F�b�N
#-------------------------------------------------
sub spambot {
	my $flag = 0;
	open(IN, "$denyfile");
	eval { flock(IN, 1); };
	while (<IN>) {
		if( $_ =~ /^\s*(\S+)/ ){
			my $part = $1;
			if( $part =~ /\d+\.\d+\.\d+\.\d+/ ){
				if($part && index( $addr, $part ) >= $[ ){
					$flag = 1;
					last;
				}
			}
		}
	}
	close (IN);
	if ($flag) { &cgi_error; }
}

#-------------------------------------------------
#  ���ݓ����擾
#-------------------------------------------------
sub get_date {
	$times = shift;
	if (!$times) { $ENV{'TZ'} = "JST-9"; $times = time; }
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);
	local(@week) = ('��','��','��','��','��','��','�y');

	# �����̃t�H�[�}�b�g
	$date = sprintf("%2d��%2d��(%s) %2d��%2d��",
			$mon+1,$mday,$week[$wday],$hour,$min);
}

#------------------------------------
#  Auto Close
#------------------------------------
sub autoclose {
	print <<EOM;
<div align="left">
<input type="button" value="&lt;&lt; TOP" onclick=window.open("$homepage","_top") class="post">
</div>
<br>
<div align="center">
<h2>�f���̗��p���Ȃ����ߕ����ł��B�Ǘ��҂܂ł��₢���킹�������B</h2>
<p>
<form action="$admincgi" method="post">
<input type="hidden" name="mode" value="admin">
�Ǘ�PASS: <input type="password" name="pass" size="12">
<input type="submit" value=" �F�� "></form>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �_�~�[�t�H�[��
#-------------------------------------------------
sub pseudo {
	if ($keitai eq 'p') {
		print qq|<br>\n<b style|;
		print qq|="font-size:24px; color:#ff0000; background-color:#ffffff; text-align: center;" |;
		print qq|class="topdisp">���̃t�H�[������͓��e�ł��܂���B</b>|;
		print qq|\n<form action="$bbscgi" method="$method" class="topdisp">\n|;
		print qq|<input type="hidden" name="mode" value="wana" class="topdisp">\n|;
		print qq|<table class="topdisp"><tr class="topdisp"><td class="topdisp">name</td>\n|;
		print qq|<td class="topdisp"><input type="text" name="name" size="28" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">e-mail</td>\n|;
		print qq|<td class="topdisp"><input type="text" name="email" size="28" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">url</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<input type="text" name="url" size="36" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">subject</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<input type="text" name="subject" size="36" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">comment</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<textarea name="comment" cols="56" rows="7" wrap="soft" class="topdisp"></textarea></td></tr>\n|;
		print qq|<tr class="topdisp"><td colspan="2" class="topdisp">\n|;
		print qq|<input type="submit" value="Write" class="topdisp">\n|;
		print qq|<input type="reset" value="Reset" class="topdisp">\n|;
		print qq|</tr></table>\n|;
		print qq|</form>\n\n|;
	}
}



1;


