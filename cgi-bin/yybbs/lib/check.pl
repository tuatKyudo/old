#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� check.pl - 2006/11/14
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<ul>
EOM

	# ���O�`�F�b�N
	my %path = (
		$logfile => "���O�t�@�C��",
		$cntfile => "�J�E���g�t�@�C��",
		);
	foreach ( keys(%path) ) {
		# �p�X
		if (-e $_) {
			print "<li>$path{$_}�p�X : OK\n";

			# �p�[�~�b�V����
			if (-r $_ && -w $_) {
				print "<li>$path{$_}�p�[�~�b�V���� : OK\n";
			} else {
				print "<li>$path{$_}�p�[�~�b�V���� : NG\n";
			}
		} else {
			print "<li>$path{$_}�p�X : NG �� $_\n";
		}
	}

	# �ߋ����O
	print "<li>�ߋ����O�F";
	if ($pastkey == 0) {
		print "�ݒ�Ȃ�\n";
	} else {
		print "�ݒ肠��\n";

		# NO�t�@�C��
		if (-e $nofile) {
			print "<li>NO�t�@�C���p�X�FOK\n";
		} else {
			print "<li>NO�t�@�C���̃p�X�FNG �� $nofile\n";
		}
		if (-r $nofile && -w $nofile) {
			print "<li>NO�t�@�C���p�[�~�b�V�����FOK\n";
		} else {
			print "<li>NO�t�@�C���p�[�~�b�V�����FNG �� $nofile\n";
		}

		# �f�B���N�g��
		if (-d $pastdir) {
			print "<li>�ߋ����O�f�B���N�g���p�X�FOK\n";
		} else {
			print "<li>�ߋ����O�f�B���N�g���̃p�X�FNG �� $pastdir\n";
		}
		if (-r $pastdir && -w $pastdir && -x $pastdir) {
			print "<li>�ߋ����O�f�B���N�g���p�[�~�b�V�����FOK\n";
		} else {
			print "<li>�ߋ����O�f�B���N�g���p�[�~�b�V�����FNG �� $pastdir\n";
		}
	}

	print <<EOM;
<li>�o�[�W���� : $ver
</ul>
</body>
</html>
EOM
	exit;
}


1;

