#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� howto.pl - 2006/11/14
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� Modified by isso. 2007
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  ���ӎ���
#-------------------------------------------------
sub howto {
	&header;
	print <<EOM;
<div align="center">
<table width="90%" border="$border" cellspacing="$cellspacing" cellpadding="10" class="thread">
<tr><td bgcolor="$tblcol">
<h3>���ӎ���</h3>
<ol>
<li>���̌f����<b>�N�b�L�[�Ή�</b>�ł��B1�x�L���𓊍e���������ƁA�����O�A�d���[���A�Q�Ɛ�A�폜�L�[�̏���2��ڈȍ~�͎������͂���܂��B�i���������p�҂̃u���E�U���N�b�L�[�Ή��̏ꍇ�j
<li>���e���e�ɂ́A<b>�^�O�͈�؎g�p�ł��܂���B</b>
<li>�L���𓊍e�����ł̕K�{���͍��ڂ�<b>�u�����O�v</b>��<b>�u���b�Z�[�W�v</b>�ł��B�d���[���A�Q�Ɛ�A�薼�A�폜�L�[�͔C�ӂł��B
<li>�L���ɂ́A<b>���p�J�i�͈�؎g�p���Ȃ��ŉ������B</b>���������̌����ƂȂ�܂��B
<li>�L���̓��e����<b>�u�폜�L�[�v</b>�ɔC�ӂ̃p�X���[�h�i�p������8�����ȓ��j�����Ă����ƁA���̋L���͎���<b>�폜�L�[</b>�ɂ���ďC���y�э폜���邱�Ƃ��ł��܂��B
<li>�L���̕ێ�������<b>�ő�$max��</b>�ł��B����𒴂���ƌÂ����Ɏ����폜����܂��B
<li>�����̋L����<b>�u�ԐM�v</b>�����邱�Ƃ��ł��܂��B�e�L���̏㕔�ɂ���<b>�u�ԐM�v</b>�{�^���������ƕԐM�p�t�H�[��������܂��B
<li>�ߋ��̓��e�L������<b>�u�L�[���[�h�v�ɂ���ĊȈՌ������ł��܂��B</b>�g�b�v���j���[��<a href="$bbscgi?mode=find&list=$in{'list'}">�u���[�h�����v</a>�̃����N���N���b�N����ƌ������[�h�ƂȂ�܂��B
<li>�Ǘ��҂��������s���v�Ɣ��f����L���⑼�l���排�������L���͗\\���Ȃ��폜���邱�Ƃ�����܂��B
</ol>
<p>
�����ł̒ǉ��@�\\
<ol>
<li>�Ǝ��̔��������Ɍf���X�p���𔻒肵���e�r�������Ă��܂��B
<li>�g�т���̉{���A���e�A�ҏW���ł��܂��B
<li>���s�L���𓊍e���ꂽ���ɕ\\��(�V�����\\��)���邱�Ƃ��ł��܂��B
<li>���e�^�C�g�����N���b�N����Ɗ֘A�X���b�h���s�b�N�A�b�v�ł��܂��B
</ol>
</td></tr></table>
<p>
<form>
<input type="button" value="�f���ɖ߂�" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  JavaScript����
#-------------------------------------------------
sub noscript {
	&header;
	print <<EOM;
<table width="100%" border="$border" cellspacing="$cellspacing" cellpadding="$cellpadding" class="thread">
<tr><th bgcolor="$tCol">
  <font color="$tblcol">JavaScript�𗘗p�������[���A�h���X�\\���ɂ���</font>
</th></tr></table>
<p><div align="center">
�X�p��(����I���f���[��)����уE�C���X�΍�̂��߁AJavaScript�𗘗p�������[���A�h���X�\\�����̗p���Ă��܂��B<br>
���萔�����������܂����A���e�҂̃��[���A�h���X��\\�������邽�߂ɂ́AJavaScript��L���ɂ��Ă��������B<br>
<br>
<form action="$bbscgi" target="_top">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="list" value="$in{'list'}">
<input type="submit" value="�f���֖߂�">
</form>
</div>
<br><hr>
</body>
</html>
EOM
	exit;
}


1;

