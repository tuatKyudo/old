#��������������������������������������������������������������������
#�� editlog.pl for YY-BOARD
#�� YY-BOARD Antispam Version Modified by isso.
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  �L���폜
#-------------------------------------------------
sub dele {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("�L��No�܂��͍폜�L�[�����̓����ł�"); }

	my ($flg, $pw2, @new);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;
	while (<DAT>) {
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw) = split(/<>/);

		if ($in{'no'} == $no) {
			$flg++;
			$pw2 = $pw;
			next;
		} elsif ($in{'no'} == $reno) {
			next;
		}
		push(@new,$_);
	}

	if (!$flg) {
		close(DAT);
		&error("�Y���̋L������������܂���");
	}
	if ($pw2 eq "") {
		close(DAT);
		&error("�폜�L�[���ݒ肳��Ă��܂���");
	}
	if (&decrypt($in{'pwd'}, $pw2) != 1) {
		close(DAT);
		&error("�폜�L�[���Ⴂ�܂�");
	}

	# �X�V
	unshift(@new,$top);
	seek(DAT, 0, 0);
	print DAT @new;
	truncate(DAT, tell(DAT));
	close(DAT);

	# �������b�Z�[�W
	&message("�폜���������܂���");
}

#-------------------------------------------------
#  �L���C��
#-------------------------------------------------
sub edit {
	if ($in{'no'} eq '' || $in{'pwd'} eq '') {
		&error("�L��No�܂��͍폜�L�[�����̓����ł�");
	}

	# �C�����s
	if ($in{'job'} eq "edit" || $in{'kaction'} eq "edit") {

		# �t�H�[�����̓`�F�b�N
		&formCheck('edit');

		# �`�F�b�N
		if ($no_wd) { &no_wd; }
		if ($jp_wd) { &jp_wd; }
		if ($urlnum > 0) { &urlnum; }

		# �Ǘ��ҍ��̃`�F�b�N
		my $acflag = 0;
		foreach (split(/\,/, $AdminName)) {
			if ($in{'name'} =~ /\Q$_\E/i) { $acflag=1; last; }
		}
		if ($adminchk && $acflag) { &error("$in{'name'}�𖼏�邱�Ƃ͂ł��܂���B"); }

		# �Ǘ��҃`�F�b�N
		my $aflag = 0;
		if ($in{'name'} eq $admin_id && $in{'pwd'} eq $pass) {
			$ccolor = $in{'color'}; @color = split(/\s+/, $color); $acol = $#color+1;
			$in{'color'} = $acol; $col[$acol] = $a_color;
			$in{'name'} = $a_name; $aflag = 1;
		}

		my $flag = 0;
		if (-e $spamdata) {
			# �֎~URL�f�[�^�����[�h
			open(SPAM,"$spamdata") || &error("Open Error : $spamdata");
			my $SPM = <SPAM>;
			close(SPAM);
			# �֎~URL�̏������݂��`�F�b�N
			foreach (split(/\,/, $SPM)) {
				if(length($_) > 1) {
					if ($in{'comment'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $in{'name'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $in{'url'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $ngmail && $in{'email'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $ngtitle && $in{'sub'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
				}
			}
		}
		if ($flag) { &error("�֎~���[�h���܂܂�Ă��܂�"); }

		my ($flg, $pw2, @new);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		my $top = <DAT>;
		while (<DAT>) {
			chomp;
			my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg++;
				$pw2 = $pw;
				$_ = "$no<>$reno<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pw<>$col[$in{'color'}]<>$in{'icon'}<>$tm<>$in{'smail'}<>";
			}
			push(@new,"$_\n");
		}

		if (!$flg) {
			close(DAT);
			&error("�Y���̋L������������܂���");
		}
		if ($pw2 eq "") {
			close(DAT);
			&error("�폜�L�[���ݒ肳��Ă��܂���");
		}

		if (&decrypt($in{'pwd'}, $pw2) != 1) {
			close(DAT);
			&error("�폜�L�[���Ⴂ�܂�");
		}

		# �X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		if($keitai ne 'p') {
			&k_after;
		} else {
			# �������b�Z�[�W
			&message("�C�����������܂���");
		}
	}

	$flag=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);
		if ($in{'no'} == $no) {
			$pw2 = $pw;
			$flag = 1;
			last;
		}
	}
	close(IN);
	if (!$flag) { &error("�Y���̋L������������܂���"); }
	if ($pw2 eq "") { &error("�폜�L�[���ݒ肳��Ă��܂���"); }

	$check = &decrypt($in{'pwd'}, $pw2);
	if ($check != 1) { &error("�폜�L�[���Ⴂ�܂�"); }

	$com =~ s/<br>/\n/g;
	$pattern = 'https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$pattern" target="_blank">($pattern)<\/a>/$1/go;

	if($keitai ne 'p') {
		&k_form("edit",$no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$in{'pwd'},$col,$ico,$tm,$sm);
	} else {
		if ($ImageView == 1) { &header('ImageUp'); }
		else { &header; }
		print <<EOM;
<form>
<input type=button value="�O��ʂɖ߂�" onClick="history.back()">
</form>
���ύX���镔���̂ݏC�����đ��M�{�^���������ĉ������B
<p>
<form action="$registcgi" method="$method">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="job" value="edit">
<input type="hidden" name="pwd" value="$in{'pwd'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="reno" value="$in{'reno'}">
<input type="hidden" name="list" value="$in{'list'}">
EOM
		# �Ǘ���
		my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
		if ($adminchk) {
			if ($cnam eq $admin_id && $cpwd eq $pass) {
				$nam = $admin_id;
				if($a_color) { $col = $a_color; }
			}
		}

		# �C���t�H�[��
		require $formpl;
		&form($nam,$eml,$url,'??',$ico,$col,$sub,$com,$sm);
		print <<EOM;
</form>
</body>
</html>
EOM
	}
	exit;
}



1;
