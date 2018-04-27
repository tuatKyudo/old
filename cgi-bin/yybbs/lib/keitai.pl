#��������������������������������������������������������������������
#�� keitai.pl for YY-BOARD ver 2.00
#�� Copyright isso. April, 2008
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#------------------#
#  �V�����ꗗ�\��  #
#------------------#
sub k_new {
	my (%no,%reno,%sub);

	if ($mode eq "k_admin") {
		if ($in{'pass'} eq "") { &enter; }
		if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }
	}

	my $i = 0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval { flock(IN, 1); };
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$d,$n,$e,$sub) = split(/<>/);
		$no{$i}    = $no;
		$reno{$i}  = $reno;
		$sub{$i}   = $sub;
		$i++;
	}
	close(IN);

	&header;
	print qq|$title\n<hr>\n|;
	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|$keitai_mode\n<br>\n|;
	}
	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="submit" value="�f���֖߂�">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klist">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�e�L��">\n</form>\n<br>\n|;
		print qq|<form action="$admincgi" method="$method">\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=klist">�e�L����</a>/\n|;
		print qq|<a href="$bbscgi?mode=newpost">���e</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">�Ǘ�</a>\n<hr>\n|;
	}

	# �\�[�g����
	my $j = 0;
	my $page = $in{'page'};
	foreach (sort { ($no{$b} <=> $no{$a}) } keys(%no)) {
		$j++;
		if ($j < $page + 1) { next; }
		if ($j > $page + $keitai_page) { next; }
		if ($reno{$_} eq '') { 
			print qq|$treehead|;
		} else {
			print qq|$cohead|;
		}
		if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
			print qq|<input type="checkbox" name="no" value="$no{$_}">�폜 |;
			print qq|[$no{$_}] <a href="$bbscgi?mode=kaview&no=$no{$_}&kmode=admin">$sub{$_}</a><br>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=kmsgview&no=$no{$_}">$sub{$_}</a><br>\n|;
		}
	}

	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<br>\n<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|�p�X���[�h: <input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="job" value="dele">\n|;
		print qq|<input type="submit" value="�폜">\n</form>\n|;
	}

	my $next = $page + $keitai_page;
	my $back = $page - $keitai_page;

	print qq|<hr>\n|;
	if ($back >= 0) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$back">\n|;
		print qq|<input type="submit" value="�O���">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="submit" value="�����">\n</form>\n|;
	}

	print qq|$copyright\n|;
	print qq|</body>\n</html>\n|;
	exit;
}

#--------------------#
#  �^�C�g���ꗗ�\��  #
#--------------------#
sub k_list {
	my (%no,%reno,%sub,%num,%cnt);

	if ($mode eq "k_admin") {
		if ($in{'pass'} eq "") { &enter; }
		if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }
	}

	my $i = 0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval { flock(IN, 1); };
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$d,$n,$e,$sub) = split(/<>/);
		if ($reno eq '') {
			$no{$i}    = $no;
			$reno{$i}  = $reno;
			$sub{$i}   = $sub;
			$num{$i}   = $i;
			$i++;
			$cnt{$no} = 0;
		} else { $cnt{$reno}++; }
	}
	close(IN);

	&header;
	print qq|$title\n<hr>\n|;
	if ($in{'pass'} eq $pass || $in{'kmode'} eq "admin") {
		print qq|$keitai_mode\n<br>\n|;
	}
	if ($in{'pass'} eq $pass || $in{'kmode'} eq "admin") {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="submit" value="�f���֖߂�">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="knew">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�V����">\n</form>\n<br>\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=knew">�V����</a>/\n|;
		print qq|<a href="$bbscgi?mode=newpost">���e</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">�Ǘ�</a>\n<hr>\n|;
	}

	# �\�[�g����
	my $j = 0;
	my $page = $in{'page'};
	foreach (sort { ($num{$a} <=> $num{$b}) } keys(%num)) {
		$j++;
		if ($j < $page + 1) { next; }
		if ($j > $page + $keitai_page) { next; }
		if ($reno{$_} eq '') {
			print qq|$treehead|;
		} else {
			print qq|$cohead|;
		}
		if ($in{'pass'} eq $pass || $in{'kmode'} eq "admin") {
			print qq|[$no{$_}] <a href="$bbscgi?mode=klview&kmode=admin&no=$no{$_}">$sub{$_}</a>\n<br>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=klview&no=$no{$_}">$sub{$_}</a> ($cnt{$no{$_}}��)\n<br>\n|;
		}
	}
	my $next = $page + $keitai_page;
	my $back = $page - $keitai_page;

	print qq|<hr>\n|;
	if ($back >= 0) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$back">\n|;
		print qq|<input type="submit" value="�O���">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="submit" value="�����">\n</form>\n|;
	}

	print qq|$copyright|;
	print qq|</body></html>\n|;
	exit;
}

#----------------------#
#  �X���b�h�����\��  #
#----------------------#
sub k_view {
	my (%no,%reno,%sub);
	my $i = 0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval { flock(IN, 1); };
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$d,$n,$e,$sub) = split(/<>/);
		if ($in{'no'} eq $reno || $in{'no'} eq $no) {
			$no{$i}    = $no;
			$reno{$i}  = $reno;
			$sub{$i}   = $sub;
			$i++;
		}
	}
	close(IN);

	&header;
	print qq|$title\n<hr>\n|;
	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|$keitai_mode\n<br>\n|;
	}
	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="submit" value="�f���֖߂�">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klist">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�e�L����">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n\n|;
		print qq|<input type="hidden" name="mode" value="knew">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�V����">\n</form>\n<br>\n|;
		print qq|<form action="$admincgi" method="$method">\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=klist">�e�L����</a>/\n|;
		print qq|<a href="$bbscgi?mode=knew">�V����</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">�Ǘ�</a>\n<hr>\n|;
	}

	# �\�[�g����
	my $j = 0;
	my $page = $in{'page'};
	foreach (sort { ($no{$a} <=> $no{$b}) } keys(%no)) {
		$j++;
		if ($j < $page + 1) { next; }
		if ($j > $page + $keitai_page) { next; }
		if ($reno{$_} eq '') {
			print qq|$treehead|;
		} else {
			print qq|$thcohead|;
		}
		if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
			print qq|<input type="checkbox" name="no" value="$no{$_}">�폜 |;
			print qq|[$no{$_}] <a href="$bbscgi?mode=kaview&kmode=admin&no=$no{$_}">$sub{$_}</a>\n<br>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=kmsgview&no=$no{$_}">$sub{$_}</a>\n<br>\n|;
		}
	}

	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<br>\n<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="job" value="dele">\n|;
		print qq|�p�X���[�h: <input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�폜">\n</form>\n|;
	}

	my $next = $page + $keitai_page;
	my $back = $page - $keitai_page;

	print qq|<hr>\n|;
	if ($back >= 0) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klview">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$back">\n|;
		print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
		print qq|<input type="submit" value="�O���">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klview">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
		print qq|<input type="submit" value="�����">\n</form>\n|;
	}

	print qq|$copyright\n|;
	print qq|</body>\n</html>\n|;
	exit;
}

#------------------#
#  ���b�Z�[�W�\��  #
#------------------#
sub k_msg {
	&header;
	print qq|$title\n<hr>\n|;
	if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
		print qq|$keitai_mode\n<br>\n|;
	}
		if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
			print qq|<a href="$bbscgi?mode=klist&kmode=admin">�e�L����</a>/\n|;
			print qq|<a href="$bbscgi?mode=knew&kmode=admin">�V����</a>\n<hr>\n|;
		} else {
			print qq|<a href="$khome">TOP</a>/\n|;
			print qq|<a href="$bbscgi?mode=klist">�e�L����</a>/\n|;
			print qq|<a href="$bbscgi?mode=knew">�V����</a>/\n|;
			print qq|<a href="$bbscgi?mode=k_admin">�Ǘ�</a>\n<hr>\n|;
		}

	my $i = 0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval { flock(IN, 1); };
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$dat,$name,$mail,$sub,$msg,$url,$h,$pw,$color,$ico,$tm,$sml) = split(/<>/);
		if ($in{'no'} eq $no) {
			my $oya = $no;
			if($reno) {
				$oya = $reno;
			}
			# �^�C�g��
			$res_sub = $sub;
			$res_sub =~ s/<([^>]|\n)*>//g;
			if ($res_sub =~ /^Re(.*)/) { $res_sub = "Re$1"; }
			else { $res_sub = "Re: $res_sub"; }
			# URL���������N
			if ($k_link) { $msg = &auto_link($msg); }
			# ���p���F�ύX
			if ($refcol) {
				$msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
			}
			# �R�����g�F�ύX
			$msg = "<font color=\"$color\">$msg</font>";
			print qq|No\.$no<br>\n$dat<br>\n�薼: $sub<br>\n���e��: $name\n<hr>\n|;
			print qq|<font color="$color">$msg</font>\n|;
			if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
				print qq|<form action="$admincgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="admin">\n|;
				print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
				print qq|<input type="hidden" name="job" value="dele">\n|;
				print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
				print qq|<input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
				print qq|<input type="submit" value="�폜">\n</form>\n|;
			} else {
				print qq|<form action="$bbscgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="newpost">\n|;
				print qq|<input type="hidden" name="kaction" value="comment">\n|;
				print qq|<input type="hidden" name="res_sub" value="$res_sub">\n|;
				print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
				print qq|<input type="hidden" name="oya" value="$oya">\n|;
				print qq|<input type="submit" value="�ԐM">\n</form>\n|;
				print qq|<form action="$bbscgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="klview">\n|;
				print qq|<input type="hidden" name="no" value="$oya">\n|;
				print qq|<input type="hidden" name="page" value="$in{'page'}">\n|;
				print qq|<input type="submit" value="���X�g�ɂ��ǂ�">\n</form>\n|;
			}
		}
	}
	close(IN);

	if ($mode eq "kmsgview") { &edit_form; }
	print qq|</body>\n</html>\n|;
	exit;
}

#----------------#
#  ���e�t�H�[��  #
#----------------#
sub k_form{
	# �N�b�L�[���擾
	my ($cname,$cmail,$curl,$cpwd,$cico,$ccol) = &get_cookie;

	my $access = &encode_bbsmode();
	my $enaddress = &encode_addr();
	if ($keychange && $_[0] ne "edit") {
		$url_key  = 'email'; $mail_key = 'url'; $name_key = 'comment'; $comment_key = 'name';
	} else { $url_key  = 'url'; $mail_key = 'email'; $name_key = 'name'; $comment_key = 'comment'; }

	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	&header;
	print qq|[<a href="$bbscgi">�f���֖߂�</a>]\n|;
	# �C����
	if ($_[0] eq "edit") {
		($edittype,$no,$reno,$date,$cname,$cmail,$res_sub,$res_msg,$curl,$host,$pw,$col,$ico,$tm,$sm) = @_;

		print qq|�C���t�H�[��<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<!-- //\n<input type="hidden" name="mode" value="write">\n// -->\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<input type="hidden" name="mode" value="edit">\n|;
		print qq|<input type="hidden" name="kaction" value="edit">\n|;
		print qq|<input type="hidden" name="pwd" value="$pw">\n|;
		print qq|<input type="hidden" name="no" value="$no">\n|;
		print qq|<input type="hidden" name="reno" value="$reno">\n|;
	# �ԐM��
	} elsif ($in{'kaction'} eq 'comment') {
		$res_sub = $in{'res_sub'};
		print qq|<hr>- �ԐM�t�H�[�� -<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<!--    //\n<input type="hidden" name="mode" value="write">\n//     -->\n|;
		print qq|<input type="hidden" name="page" value="$page">\n|;
		print qq|<input type="hidden" name="kaction" value="res_msg">\n|;
		print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
		print qq|<input type="hidden" name="reno" value="$in{'oya'}">\n|;
	# �V�K��
	} else {
		print qq|<hr>- �V�K���e�t�H�[�� -<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<!--    //\n<input type="hidden" name="mode" value="write">\n//     -->\n|;
	}

	if ($allowmode) {
		if ($_[0] ne "edit" && $in{'kaction'} ne "comment") {
			print qq|<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>\n<br>\n|;
		}
	}

	print qq|���Ȃ܂� <input type="text" name="$name_key" size="20" value="$cname"><br>\n|;

	if ($aikotoba) {
		print qq|<b>�������t</b><br>\n|;
		print qq|<input type="text" name="aikotoba" size="10" value="$caikotoba">|;
		print qq|<font color="#ff0000">���K�{</font><br>\n|;
		print qq|$hint<br>\n|;
	}

	print qq|�d���[�� <input type="hidden" name="mail" size="28" value="$enaddress">\n|;
	print qq|<input type="text" name="$mail_key" size="20" value="$cmail">\n|;
	if ($in_email) {
		print qq|<font color="#ff0000">�K�{</font>\n|;
	}
	print qq|<br>\n|;

	print qq|�^�C�g�� <input type="text" name="sub" size="20" value="$res_sub">\n|;
	print qq|\n<!-- //\n<input type="text" name="subject" size="36" value="">\n// -->\n|;
	print qq|<input type="hidden" name="title" size="36" value="">\n|;
	print qq|<input type="hidden" name="theme" size="36" value="">\n<br>\n|;

	if ($topsort) {
		if ($in{'kaction'} eq 'comment') {
				print qq|<input type="checkbox" name="sage" value="1"> sage\n<br>\n|;
		}
	}

	my $f_c_d = int(rand(5E07)) + 12E08;
	print qq|URL <!--//\n  URL\n<input type="text" name="url2" size="50" value="">\n//-->\n|;
	print qq|<input type="hidden" name="$formcheck" value="$f_c_d">\n|;
	print qq|<input type="text" name="$url_key" size="20" value="$curl"><br>\n|;

	print qq|<input type="hidden" name="smail" value="$sm">\n|;

	print qq|���b�Z�[�W<br>\n|;
	print qq|<textarea name="$comment_key" rows="5" cols="20" wrap="soft">$res_msg</textarea><br>\n|;

	# �Ǘ��҃A�C�R����z��ɕt��
	@ico1 = split(/\s+/, $ico1);
	@ico2 = split(/\s+/, $ico2);
	if ($my_icon) {
		push(@ico1,$my_gif);
		push(@ico2,"�Ǘ��җp");
	}
	if ($iconMode) {
		print qq|�A�C�R�� <select name="icon">\n|;
		foreach(0 .. $#ico1) {
			if ($ico eq $ico1[$_]) {
				print qq|<option value="$_" selected>$ico2[$_]\n|;
			} else {
				print qq|<option value="$_">$ico2[$_]\n|;
			}
		}
		print qq|</select> &nbsp;\n|;
		print qq|<br>\n|;
	}

	# �F���
	print qq|�F \n|;
	my @col = split(/\s+/, $color);
	if ($col eq "") { $col = 0; }
	my $acol = $#col;
	# �Ǘ��ҐF
	if ($adminchk && $nam eq $admin_id) {
		$acol = $#col+1; $col[$acol] = $a_color;
	}
	foreach (0 .. $acol) {
		if ($col eq $col[$_] || $col eq $_) {
			print qq|<input type="radio" name="color" value="$_" checked>|;
			print qq|<font color="$col[$_]">��</font>\n|;
		} else {
			print qq|<input type="radio" name="color" value="$_">|;
			print qq|<font color="$col[$_]">��</font>\n|;
		}
	}
	print qq|<br>\n|;

	if ($_[0] eq "edit") {
		print qq|<input type="submit" value=" �L�����C������ "></form><br>\n|;
	} else {
		print qq|�폜�L�[ <input type="password" name="pwd" size="8" value="$cpwd" maxlength=\8\>\n|;
		if ($in_pwd) {
			print qq|<b><font color="#ff0000">���K�{</font></b>|;
		}
		print qq|<br>(�p������8�����ȓ�)<br>\n|;
		if ($regist_key) {
			print qq|<input type="text" name="regikey" size="6" style="ime-mode:inactive" value="">\n<br>\n|;
			print qq|�i���e�� <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="���e�L�[">|;
			print qq| ����͂��Ă��������j<br>\n|;
			print qq|<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
		}
		print qq|<input type="hidden" name="mode" value="$writevalue">\n|;
		print qq|<input type="submit" name="submit" value=" �L���𓊍e���� "></form>\n|;
	}
	print qq|</body>\n</html>\n|;
	exit;
}

#------------#
#  �������  #
#------------#
sub enter {
	&header;
	print <<EOM;
<a href="$bbscgi">�f���֖߂�</a>
<hr>
�Ǘ��҃p�X���[�h: 
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="k_admin">
<input type="hidden" name="kmode" value="admin">
<input type="password" name="pass" size="8">
<input type="submit" value=" �F�� "></form>
</body>
</html>
EOM
	exit;
}

#------------#
#  �L���폜  #
#------------#
sub k_dele {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �폜�����}�b�`���O
	$new = ();
	$flag = 0;
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval { flock(DAT, 2); };
	$top = <DAT>;
	while (<DAT>) {
		($no,$re) = split(/<>/);
		foreach $del ( split(/\0/, $in{'no'}) ) {
			if ($no == $del || $re == $del) {
				$flag = 1; last;
			}
		}
		if ($flag == 0) { push(@new,$_); }
	}

	# ���O���X�V
	unshift(@new,$top);
	seek(DAT, 0, 0);
	print DAT @new;
	truncate(DAT, tell(DAT));
	close(DAT);

	&header;
	print <<EOM;
<form action="$bbscgi" method="$method">
<input type="submit" value="�f���֖߂�">
</form>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="knew">
<input type="hidden" name="kmode" value="$in{'kmode'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="�Ǘ����[�h">
</form>
</body>
</html>
EOM
	exit;
}

#----------------#
#  �C���t�H�[��  #
#----------------#
sub edit_form {
	print <<EOM;
<hr>
- �L���̏C���E�폜 - <br>
<form action="$registcgi" method="$method">
�����I�� <select name="mode">
<option value="edit">�C��
<option value="dele">�폜</select><br>
�L��No. <input type="text" name="no" size="6" value="$in{'no'}"><br>
�폜�L�[ <input type="password" name="pwd" size="8" value=""></small>
<input type="submit" value="���s"></form>
<hr>
$copyright
EOM
	exit;
}

#----------------#
#  �������݊���  #
#----------------#
sub k_after {
	&header;
	print qq|<a href="$bbscgi">�f���֖߂�</a>\n|;
	print qq|</body></html>\n|;
	exit;
}

1;
