#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� read.cgi - 2007/09/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��
#�� YY-BOARD Antispam Version Modified by isso.
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

# �O���t�@�C���捞
require './init.cgi';
require $jcode;

#-------------------------------------------------
# �ݒ�`�F�b�N
#-------------------------------------------------
# ���O�t�@�C��
unless(-e "$logfile") {
	&error("���O�t�@�C�� $logfile ������܂���B");
}

# �ߋ����O�f�[�^�t�@�C��
if($pastkey) {
	unless(-e "$nofile") {
		&error("�ߋ����O�f�[�^�t�@�C�� $nofile  ������܂���B");
	}
}

# �J���[�f�[�^�t�@�C��
if (-e "$colorfile") {
	open(COL,"$colorfile");
	$boardmode = <COL>;
	close(COL);
} else {
	open(OUT,">>$colorfile");
	print OUT "0";
	close(OUT);
	$boardmode = 0;
}
unless(-e "$colordata") {
	&error("�J���[�f�[�^�t�@�C�� $colordata ������܂���B");
}

# �\�����[�h�ݒ�
if ($boardmode && -s "$colordata") { &read_color; }

#-------------------------------------------------
# ���C������
#-------------------------------------------------
&agent;
&decode;
&axsCheck;

# ������
if ($clday) {
	my $last = (stat $logfile)[9];
	if (abs(time - $last) > $clday*24*3600) {
		&header;
		&pseudo;
		&autoclose;
	}
}

&read_log;

#-------------------------------------------------
#  �L���ʉ{��
#-------------------------------------------------
sub read_log {
	# �L����W�J
	local($data,@tree);
	open(IN,"$logfile") || &error("Open Error: $logfile");
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($in{'no'} == $no) { $data = $_; }
		if ($in{'no'} == $no || $in{'no'} == $reno || ($in{'top'} && ($in{'top'} == $no || $in{'top'} == $reno))) {
			push(@tree,$_);
		}
	}
	close(IN);

	if (!$data) { &error("�s���ȃA�N�Z�X�ł�"); }

	# �w�b�_���o��
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# �^�C�g����
	print qq|<div align="center">\n|;
	if ($banner1 ne "<!-- �㕔 -->") { print "$banner1<p>\n"; }
	if ($t_img eq '') {
		print qq|<b style="color:$tCol; font-size:$tSize;">$title</b>\n|;
	} else {
		print qq|<img src="$t_img" width="$t_w" height="$t_h" alt="$title">\n|;
	}

	if ($boardmode) {
#		if (!defined($list_type{$in{'list'}})) { $in{'list'} = $view_type; }

		print qq|<table border="0" width="500"><tr>\n|;
		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="hidden" name="page" value="$in{'page'}">\n|;
		print qq|<input type="submit" value="���X�g�ɖ߂�" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$homepage" method="get">\n<td nowrap>\n|;
		print qq|<input type="submit" value="�z�[���ɖ߂�" class="menu">\n</td>\n</form>\n|;

		# �V�K���e
		if (!$in{'list'}) { $in{'list'} = 'thread'; }
		if ($in{'list'} ne "thread") {
			print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
			print qq|<input type="hidden" name="mode" value="postform">\n|;
			print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
			print qq|<input type="submit" value="�V�K���e" class="menu">\n</td>\n</form>\n|;
		}

		foreach ( 'thread', 'tree', 'topic', 'new' ) {
			next if ($in{'list'} eq $_);
			print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
			print qq|<input type="hidden" name="list" value="$_">\n|;
			print qq|<input type="submit" value="$list_type{$_}" class="menu">\n</td>\n</form>\n|;
		}

		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="howto">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="submit" value="���ӎ���" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="find">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="submit" value="���[�h����" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="past">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="submit" value="�ߋ����O" class="menu">\n</td>\n</form>\n| if ($pastkey);

		print qq|<form action="$admincgi" method="post"><td nowrap>\n\n|;
		print qq|<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="submit" value="�Ǘ��p" class="menu">\n</td>\n</form>\n|;

		print qq|</tr></table>\n|;
		print qq|</div>\n<br>\n|;

	} else {

		print <<EOM;
<hr width="90%">
[<a href="$bbscgi?list=$in{'list'}&page=$in{'page'}">���X�g�ɖ߂�</a>]
[<a href="$homepage" target="_top">�z�[���ɖ߂�</a>]
EOM

		if (!$in{'list'}) { $in{'list'} = 'thread'; }
		if ($in{'list'} ne "thread") {
			print qq|[<a href="$bbscgi?mode=form&list=$in{'list'}">�V�K���e</a>]\n|;
		}

		foreach ( 'thread', 'tree', 'topic', 'new', ) {
			next if ($in{'list'} eq $_);

			print qq|[<a href="$bbscgi?list=$_">$list_type{$_}</a>]\n|;
		}

		print <<EOM;
[<a href="$bbscgi?mode=howto&list=$in{'list'}">���ӎ���</a>]
[<a href="$bbscgi?mode=find&list=$in{'list'}">���[�h����</a>]
EOM

		# �ߋ����O�̃����N����\��
		if ($pastkey) {
			print qq|[<a href="$bbscgi?mode=past&list=$in{'list'}">�ߋ����O</a>]\n|;
		}

	print <<EOM;
[<a href="$admincgi">�Ǘ��p</a>]
<hr width="90%"></div>
EOM
	}

	# �L���ꊇ�̂Ƃ�
	if ($mode eq "all") { &all_list; }

	# �{���L��
	my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/, $data);

	# ���`
	$author = $nam;
	require $messagepl;
	$nam = &emailscript($nam,$no,$eml,$sml,$col,$hos);
	if ($url) {
		my ($part,$flg) = &short_link($url);
		$url = qq|<a href="$url" target="_blank">$part</a>|;
	}

	print qq|<blockquote>\n|;

	if ($boardmode) {
		print qq|<div align="center">\n|;
		print qq|<p><table width="90%" cellpadding="$cellpadding" cellspacing="$cellspacing" border="$border" class="thread">\n|;
		if ($thr_bg && $backgif) { print qq|<tr><td>\n|; }
		else { print qq|<tr>\n<td bgcolor="$tblcol">\n|; }
	}

	print <<EOM;
<table>
<tr>
  <td>�L��No</td><td>�F <b>$no</b></td>
</tr>
<tr>
  <td>�^�C�g��</td><td>�F <b style="color:$subcol">$sub</b></td>
</tr>
<tr>
  <td>���e��</td><td>�F $dat</td>
</tr>
<tr>
  <td>���e��</td><td>�F <b>$nam</b></td>
</tr>
EOM
	if ($url) {
		print qq|<tr>\n  <td>URL</td><td>�F $url</td>\n</tr>\n|;
	}
	print qq|</table>\n<p>\n|;

	# ���p���F�ύX
	if ($refcol) {
		$com =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
	}

	# URL���������N
	if ($autolink) { $com = &auto_link($com); }

	# �L��
	if ($iconMode) {
		print qq|<table><tr><td><img src="$imgurl/$ico"></td>\n|;
		print qq|<td width="8"></td>\n|;
		print qq|<td style="color:$col">$com</td></tr></table>\n|;
	} else {
		print qq|<div style="margin-left:22px; margin-top:6px">\n|;
		print qq|<span style="color:$col">$com</span>\n|;
	}

	local ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	# ���e�ҕҏW�t�H�[��
	if ($boardmode) {
		print qq|<form action="$registcgi" method="$method">\n|;
		if ($pw) {
			if ($cnam) {
				if ($cnam =~ /\Q$author\E/i || $author =~ /\Q$cnam\E/i) {
					print qq|<div align="right">\n|;
					print qq|���e�� <select name="mode">\n|;
					print qq|<option value="edit">�C��\n|;
					print qq|<option value="dele">�폜</select>\n|;
					print qq|<input type="hidden" name="no" value="$no">\n&nbsp;|;
					print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
					print qq|�폜�L�[ <input type="password" name="pwd" size="8" maxlength="8" value="$cpwd">\n|;
					print qq|<input type="submit" value="���M" class="post"></div>\n|;
				}
			}
		}
		print qq|</td>\n</tr>\n</table>\n</div>\n|;
		print qq|</form>\n|;
	} else {
		print qq|<hr>\n|;
	}

	print <<EOM;
<b>- �֘A�c���[</b>
<p>
EOM

	# �֘A�c���[
	my $i = 0;
	local($oya,$resub);
	foreach (@tree) {
		$i++;
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($reno && $i == @tree) {
			print "&nbsp" x 5;
			print "�� ";
		} elsif ($reno && $i > 1) {
			print "&nbsp" x 5;
			print "�� ";
		}

		my $param;
		if ($reno) {
			$param = "&top=$reno";
		} else {
			$oya = $no;
			$resub = $sub;
		}

		require $messagepl;
		$nam = &emailscript($nam,$no,$eml,$sml,$col,$hos);

		# �e
		if (!$reno) {
			print qq|<a href="$readcgi?mode=all&list=tree&no=$no" title="�c���[���ꊇ�\\��">��</a> |;
		}

		if ($in{'no'} eq $no) {
			print qq|<b style="background-color:$tree_bc"> |;
		}

		if ($in{'no'} ne $no) {
			print qq|<a href="$readcgi?list=tree&no=$no$param">$sub</a>|;
		} else { print qq|$sub|; }
		print qq| - <b>$nam</b> $dat <span style="color:$subcol">No.$no</span>\n|;
		if (time - $tm < $new_time * 3600) {
			print qq|&nbsp;$newmark\n|;
		}

		if ($in{'no'} eq $no) {
			print qq|</b> |;
		}

		print qq|<br>\n|;
	}

	&reply_form;
}

#-------------------------------------------------
#  �L���ꊇ�{��
#-------------------------------------------------
sub all_list {
	print <<EOM;
<blockquote>
EOM

	# �֘A�c���[
	my $i = 0;
	local($oya,$resub,$list);
	foreach (@tree) {
		$i++;
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($reno && $i == @tree) { print "&nbsp;�� "; }
		elsif ($reno && $i > 1) { print "&nbsp;�� "; }

		$author = $nam;
		require $messagepl;
		$nam = &emailscript($nam,$no,$eml,$sml,$col,$hos);

		my $param;
		if ($reno) {
			$param = "&top=$reno";
			$oya = $reno;
		} else {
			$oya = $no;
			$resub = $sub;
		}

		# �c���[�\��
		print qq|<a href="$readcgi?mode=all&list=$in{'list'}&no=$oya#$no">$sub</a> - <b>$nam</b> $dat <span style="color:$subcol">No.$no</span>\n|;
		if (time - $tm < $new_time * 3600) {
			print qq|&nbsp;$newmark\n|;
		}
		print qq|<br>\n|;

		# �e�L��
		if (!$reno) {
			push(@view,$no);
		# ���X�L��
		} else {
			$res{$reno} .= "$no,";
		}

		# �薼�̒���
		if (length($sub) > $sub_len*2) {
			$sub = substr($sub, 0, $sub_len*2) . "...";
		}

		$author{$no} = $author;
		$no{$no} = $no;
		$re{$no} = $reno;
		$nam{$no} = $nam;
		$eml{$no} = $eml;
		$sub{$no} = $sub;
		$dat{$no} = $dat;
		$com{$no} = $com;
		$col{$no} = $col;
		$url{$no} = $url;
		$ico{$no} = $ico;
		$pw{$no}  = $pw;
		$tm{$no}  = $tm;
		$sml{$no} = $sml;
	}

	# �N�b�L�[�擾
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	require $list_log_thread;
	&list_log_thread;

	&reply_form;
}

#-------------------------------------------------
#  �ԐM��p�t�H�[��
#-------------------------------------------------
sub reply_form {

	if ($boardmode) {
			print qq|<p>\n<br>\n|;
	} else {
			print qq|<p>\n<hr>\n|;
	}

	print <<EOM;
<b>- �ԐM�t�H�[��</b>
<p>
EOM

	# �^�C�g����
	if ($resub !~ /^Re\:/) { $resub = "Re: $resub"; }

	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

	# ���e�t�H�[��
	print qq|<form method="post" action="$registcgi">\n|;
	print qq|<!-- //\n|;
	print qq|<input type="hidden" name="mode" value="write">\n|;
	print qq|// -->\n|;
	print qq|<input type="hidden" name="page" value="$page">\n|;
	print qq|<input type="hidden" name="reno" value="$oya">\n|;
	print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
	print qq|<input type="hidden" name="num" value="$in{'num'}">\n|;

	if ($allowmode) {
		print qq|<table border="$border" cellspacing="0" class="allow">\n<tr>\n<td>\n|;
		print qq|<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>|;
		print qq|</td>\n</tr>\n</table>\n<br>\n|;
	}

	# �t�H�[��
	if (!$re_box) { $cref = 0; }
	require $formpl;
	&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$resub,'',$csmail,$caikotoba,$cref,'reply');
	print qq|</form>\n|;

	# ���[�U�����e�t�H�[���i�g�s�b�N�\���̏ꍇ�j
	if ($in{'list'} eq "topic") {
		if ($boardmode) {
			print qq|<br>\n<br>\n|;
			print qq|<b>- �L���C�����폜�t�H�[��</b><br>\n<br>\n|;
			print qq|<table border="0" cellspacing="10" cellpadding="0" class="thread">\n<tr><td>\n|;
		} else {
			print qq|<hr>\n|;
			print qq|<b>- �L���C�����폜�t�H�[��</b><br>\n<br>\n|;
		}
		print qq|<form action="$registcgi" method="post">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|���e�� <select name="mode" class="f">\n|;
		print qq|<option value="edit">�C��\n|;
		print qq|<option value="dele">�폜</select>\n|;
		print qq|No.<input type="text" name="no" size="3" class="f" style="ime-mode:inactive">\n|;
		print qq|�폜�L�[<input type="password" name="pwd" size="4" maxlength="8" value="$cpwd" class="f">\n|;
		print qq|<input type="submit" value="���M">|;
		if ($boardmode) { print qq|</td>\n</tr>\n</table>\n</form>\n|; }
	}

	print <<EOM;
</blockquote>
</body>
</html>
EOM
	exit;
}


