#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� yybbs.cgi - 2007/09/17
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
if(!$writevalue || !$postvalue) {
	&error("init.cgi�t�@�C�����������]������Ă��Ȃ����ݒ�l������������܂���B");
}
if($writevalue eq $postvalue) {
	&error("\$writevalue��\$postvalue�̕����͓����ɂ��Ȃ��ł�������");
}

# �f�[�^�p�f�B���N�g��
unless(-d "./data/") {
	mkdir ("./data/", 0707) || die "�f�B���N�g�����쐬�ł��܂��� : $!";
}

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

# �J�E���^�[�f�[�^�t�@�C��
unless(-e "$cntfile") {
	&error("�J�E���^�[�f�[�^�t�@�C�� $cntfile ������܂���B");
}

# Webmail�F�ؗp�f�B���N�g��
if($webmail){
	unless(-d "$mailchk") {
		mkdir ($mailchk, 0707) || die "�f�B���N�g�����쐬�ł��܂��� : $!";
	}
	# �f�B���N�g������|��
	opendir DIR, $mailchk;
	my @files = grep { !m/^(\.|\.\.|$sendmaillog)$/g } readdir DIR;
	close DIR;
	foreach (@files) {
		my $wt = (stat "$mailchk$_")[9];
		if (time - $wt > $maxtime) { unlink ("$mailchk$_"); }
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

# ���e�L�[�Í��p�p�X���[�h�`�F�b�N
if ($regist_key) {
	if (!$pcp_passwd) {
		&error("���e�L�[�Í��p�p�X���[�h \$pcp_passwd ���ݒ肳��Ă��܂���B");
	}
}


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

if ($mode eq "find") { &find; }
elsif ($mode eq "image") { &image; }
elsif ($mode eq "form") { require $formpl; &postform; }
elsif ($mode eq "past") { require $pastlogpl; &past_log; }
elsif ($mode eq "howto") { require $howtopl; &howto; }
elsif ($mode eq "check") { require $checkpl; &check; }
elsif ($mode eq "noscript") { require $howtopl; &noscript; }
elsif ($mode eq "writemail") { require $webmailpl; &writemail; }
elsif ($mode eq "sendmail")  { require $webmailpl; &sendmail; }
elsif ($mode eq "postform") { require $formpl; &postform; }
elsif ($mode eq "wana") { &wana; }
# �g�ёΉ�����
elsif ($keitai ne 'p' && $mode eq "knew") { &k_new; }
elsif ($keitai ne 'p' && $mode eq "klist") { &k_list; }
elsif ($keitai ne 'p' && $mode eq "klview") { &k_view; }
elsif ($keitai ne 'p' && $mode eq "kaview") { &k_msg; }
elsif ($keitai ne 'p' && $mode eq "kmsgview") { &k_msg; }
elsif ($keitai ne 'p' && $mode eq "k_admin") { &k_new; }
elsif ($keitai ne 'p' && $mode eq "newpost") { &k_form; }
elsif ($keitai ne 'p' && $mode eq "admin" && $in{'no'}) { &k_dele; }
&log_view;

#-------------------------------------------------
#  �L���\����
#-------------------------------------------------
sub log_view {
	# �g�у��[�h
	if (-e "$kscript" && $keitai ne 'p') { &k_list; }

	# �y�[�W�J�z
	local($resfm);
	foreach ( keys(%in) ) {
		if (/^page_(\d+)$/) {
			$page = $1;
		}
		if (/^res_(\d+)$/) {
			$resfm = $1;
			last;
		}
	}
	# �ԐM�t�H�[������
	if ($resfm) { &res_form; }

	# �N�b�L�[�擾
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	&set_cookie($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref);

	# �w�b�_���o��
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# �J�E���^����
	if ($counter) { &counter; }

	# �_�~�[
	&pseudo;

	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;
		($str_plain,$str_crypt) = &pcp_makekey;
	}

	# �^�C�g����
	print qq|<div align="center">\n|;
	if ($banner1 ne "<!-- �㕔 -->") { print "$banner1<p>\n"; }
	if ($t_img eq '') {
		print qq|<b style="color:$tCol; font-size:$tSize;">$title</b>\n|;
	} else {
		print qq|<img src="$t_img" width="$t_w" height="$t_h" alt="$title">\n|;
	}

	# �\���w�b�_
	print qq|$header<br>\n|;

	# �X�p�����O�`�F�b�N
	if (-s $spamlogfile) {
		open(IN,"<$spamlogfile");
		eval { flock(IN, 2); };
		my @spmlog = <IN>;
		close(IN);
		if ($#spmlog >= $spamlog_max) {
			print qq|<br>\n<br>\n|;
			print qq|<b style="color:#ff0000; background-color:#ffffff; border-top-style:solid; border-bottom-style:solid; border-width:1; padding-top: 5px; padding-bottom: 5px;">|;
			print qq|$postmode���O�����e���𒴂��܂����B�Ǘ����[�h����$postmode���O���폜���ĉ������B|;
			print qq|</b><br>\n<br>\n|;
		}
	}

	# �\�������ݒ�
	if (!$in{'list'}) { $in{'list'} = $list_ini; }

	# ���j���[��
	if ($boardmode) {
		if (!defined($list_type{$in{'list'}})) {
			if (defined($list_type{$view_type})) {
				$in{'list'} = $view_type;
			} else {
				$in{'list'} = 'thread';
			}
		}

		print qq|<table border="0" width="500"><tr>\n|;
		if ($in{'action'} eq "past") {
			print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
			print qq|<input type="submit" value="�f���ɖ߂�" class="menu">\n</td>\n</form>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=wana"><!--// �A�N�Z�X�֎~ //--></a>\n|;
			print qq|<form action="$homepage" method="get">\n<td nowrap>\n|;
			print qq|<input type="submit" value="�g�b�v�ɖ߂�" class="menu">\n</td>\n</form>\n|;
		}
		# ���e�t�H�[�������N
		if (($referercheck && !$ENV{'HTTP_REFERER'}) || !$postform) {
			if ($in{'list'} ne "pickup") {
				print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
				print qq|<input type="hidden" name="mode" value="postform">\n|;
				print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
				print qq|<input type="submit" value="�V�K���e" class="menu">\n</td>\n</form>\n|;
			}
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

		print qq|<form action="$admincgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="submit" value="�Ǘ��p" class="menu">\n</td>\n</form>\n|;

		print qq|</tr></table>\n|;
		print qq|</div>\n<br>\n|;

	} else {

		print qq|<hr width="90%">\n|;
		print qq|[<a href="$homepage" target="_top">�z�[���ɖ߂�</a>]\n|;

		# ���e�t�H�[�������N
		if (($referercheck && !$ENV{'HTTP_REFERER'}) || !$postform) {
			if ($in{'list'} ne "pickup") {
				print qq|[<a href="$bbscgi?mode=postform">�V�K���e</a>]\n|;
			}
		}

		if (!defined($list_type{$in{'list'}})) {
			if (defined($list_type{$view_type})) {
				$in{'list'} = $view_type;
			} else {
				$in{'list'} = 'thread';
			}
		}
		if ($in{'list'} ne "thread") {
			print qq|[<a href="$bbscgi?mode=form&list=$in{'list'}">�V�K���e</a>]\n|;
		}

		foreach ( 'thread', 'tree', 'topic', 'new' ) {
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

	# �^�C�g���ꗗ�\��
	if (-s $logfile) {
		if ($alltitle) {
			if ($in{'list'} eq 'thread' || $in{'list'} eq 'new') {
				&SubjectList;
			}
		}
	}

	# ���e�t�H�[��
	if ($in{'list'} eq 'thread' || $in{'list'} eq 'new') {
		if ($postform) {
			if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

			print qq|<blockquote>\n|;
			print qq|<form method="$method" action="$registcgi">\n|;
			print qq|<input type="hidden" name="page" value="$page">\n|;
			print <<EOM;
<!-- //
<input type="hidden" name="mode" value="write">
// -->
<input type="hidden" name="reno" value="$in{'no'}">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="list" value="$in{'list'}">
EOM
			if ($allowmode) {
				print qq|<table border="$border" cellspacing="0" class="allow">\n<tr>\n<td>\n|;
				print qq|<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>|;
				print qq|</td>\n</tr>\n</table>\n<br>\n|;
			}

			if (!$re_box) { $cref = 0; }
			require $formpl;
			if (!$referercheck || $ENV{'HTTP_REFERER'}) {
				&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,'',$inputform,$csmail,$caikotoba,$cref);
				print qq|</form>\n</blockquote>\n|;
			} else {
				print qq|</form>\n<br>\n<div style="text-align:center;">\n|;
				print qq|<form action="$bbscgi" method="$method">\n|;
				print qq|<input type="submit" value="�V�K���e�͂����炩�炨�肢���܂��B" class="menu">\n|;
				print qq|</form>\n</div><br>\n|;
			}
		}
		print qq|<br>\n<div align="center">\n|;
	}

	# �V�����\��
	if ($in{'list'} eq "new") { require $newsortpl; &newsort; }
	# �֘A�L���\��
	elsif ($in{'list'} eq "pickup") { require $pickuppl; &pickup; }
	else {

		# �����`�F�b�N
		if ($pglog{$in{'list'}} <= 0) { $pglog{$in{'list'}} = 10; }

		# �L����W�J
		my $i = 0;
		open(IN,"$logfile") || &error("Open Error: $logfile");
		my $top = <IN>;
		while (<IN>) {
			my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

			if ($reno eq "") { $i++; }
			if ($i < $page + 1) { next; }
			if ($i > $page + $pglog{$in{'list'}}) { next; }

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

			$author = $nam;
			require $messagepl;
			$nam = &emailscript($nam,$no,$eml,$sml,$col,$hos);

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
		close(IN);

		# �L���\��
		if ($in{'list'} eq "tree") {
			require $list_log_tree;
			&list_log_tree;

		} elsif ($in{'list'} eq "topic") {
			require $list_log_topic;
			&list_log_topic;

		} else {
			require $list_log_thread;
			&list_log_thread;
		}

		# �y�[�W�ړ��{�^���\��
		if ($page - $pglog{$in{'list'}} >= 0 || $page + $pglog{$in{'list'}} < $i) {
			print qq|<p><table width="90%" align="center">\n|;
			print qq|<tr><td class="n">Page:\n|;
			&mvbtn("$bbscgi?page=", $i, $pglog{$in{'list'}});
			print qq|</td></tr></table>\n|;
		}

		print qq|<div align="center">\n|;

	}

	# ���[�U�����e�t�H�[���i�g�s�b�N�\���ȊO�j
	if ($in{'list'} ne "topic" && $mode ne "past" && $in{'action'} ne "past") {
		if ($boardmode) {
			print qq|<table border="0" cellspacing="10" cellpadding="0" class="thread">\n<tr><td>\n|;
		}
		print qq|<form action="$registcgi" method="post">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|���e��<select name="mode" class="f">\n|;
		print qq|<option value="edit">�C��\n|;
		print qq|<option value="dele">�폜</select>\n|;
		print qq|No.<input type="text" name="no" size="3" class="f" style="ime-mode:inactive">\n|;
		print qq|�폜�L�[<input type="password" name="pwd" size="4" maxlength="8" value="$cpwd" class="f">\n|;
		print qq|<input type="submit" value="���M">|;
		if ($boardmode) { print qq|</td>\n</tr>\n</table>\n</form>\n|; }
	}

	# ���쌠�\���i�폜�s�j
	print <<EOM;
$banner2
<p>
<!-- $ver -->
<span style="font-size:10px; font-family:Verdana,Helvetica,Arial;">
- <a href="&#104;&#116;&#116;&#112;&#58;&#47;&#47;&#119;&#119;&#119;&#46;&#107;&#101;&#110;&#116;&#45;&#119;&#101;&#98;&#46;&#99;&#111;&#109;&#47;" target="_top">&#89;&#89;&#45;&#66;&#79;&#65;&#82;&#68;</a> 
EOM
	# ���쌠�\���i�폜�s�j
	print <<EOM;
<a href="&#104;&#116;&#116;&#112;&#58;&#47;&#47;&#115;&#119;&#97;&#110;&#98;&#97;&#121;&#45;&#119;&#101;&#98;&#46;&#104;&#112;&#46;&#105;&#110;&#102;&#111;&#115;&#101;&#101;&#107;&#46;&#99;&#111;&#46;&#106;&#112;&#47;&#105;&#110;&#100;&#101;&#120;&#46;&#104;&#116;&#109;&#108;" target="_top">&#x41;&#x6e;&#x74;&#x69;&#x73;&#x70;&#x61;&#x6d;&#x20;&#x56;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;</a> -
</span>
<br>
$footer
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �ԐM�t�H�[��
#-------------------------------------------------
sub res_form {
	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}
	$in{'no'} = $resfm;

	# �N�b�L�[���擾
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	# ���L�����p
	my $refcom = '';
	my $resub  = '';
	open(REF,"$logfile") || &error("Open Error: $logfile");
	my $tp = <REF>;
	while (<REF>) {
		chomp;
		my ($n,$r,$d,$na,$em,$sb,$c) = split(/<>/);
		if ($in{'refnum'} eq $n) {
			$resub = $sb;
			if ($in{'refmode'} eq "on") { $refcom = $c; last; }
		}
	}
	close(REF);

	# ���O��ǂݍ���
	my $flg;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	my $top = <IN>;

	# �w�b�_���o��
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# �֘A�L���o��
	print <<EOM;
<form>
<input type="button" value="&lt; �߂�" onclick="history.back()">
</form>
���ȉ��͋L��No.<b>$in{'no'}</b> �Ɋւ���<a href="#RES">�ԐM�t�H�[��</a>�ł��B
<div align="center">
EOM

	print "<p><table width=\"90%\" cellpadding=\"$cellpadding\" cellspacing=\"$cellspacing\" border=\"$border\" class=\"thread\">\n";
	print "<tr><td bgcolor=\"$tblcol\"><br>\n";

	while (<IN>) {
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col) = split(/<>/);
		if ($in{'no'} == $no && $reno) { $flg++; }
		if ($in{'no'} == $no || $in{'no'} == $reno) {

			if ($in{'no'} == $no) { $resub = $sub; }
			if ($url) { $url = "&lt;<a href=\"$url\">Home</a>&gt;"; }
			if ($reno) { print "<hr width=\"90%\">"; }
			if ($reno) { print '&nbsp;&nbsp;'; }

			if ($nam_col) { $nam = "<font color=\"$col\">$nam</font>"; }
			if ($refcol) {
				$com =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
			}
			# URL�����N
			if ($autolink) { $com = &auto_link($com); }

			print "<font color=\"$subcol\"><b>$sub</b></font>\n";
			if ($boardmode) {
				print "���e�ҁF<b>$nam</b> $url ";
			} else {
				print "���e�ҁF<b>$nam</b> ���e���F$dat $url ";
				print "<font color=\"$subcol\">No.$no</font><br>\n";
			}
			print "<blockquote><font color=\"$col\">$com</font></blockquote>\n";
			if ($boardmode) {
				print "<div align=\"right\">$dat \[<font color=\"$subcol\">No.$no</font>\]\n</div>\n";
			}
		}
	}
	close(IN);

	print "</td></tr></table></p></div>\n";
	if ($flg) { &error("�s���ȕԐM�v���ł�"); }

	# �^�C�g����
	if ($resub !~ /^Re\:/) { $resub = "Re: $resub"; }

	if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

	print "<blockquote>";
	print "<form action=\"$registcgi\" method=\"$method\">";
	print <<EOM;
<!-- //
<input type="hidden" name="mode" value="write">
// -->
<input type="hidden" name="page" value="$page">
<input type="hidden" name="reno" value="$in{'no'}">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="refmode" value="$in{'refmode'}">
<input type="hidden" name="num" value="$in{'num'}">
EOM

	if ($allowmode) {
		print "<table border=\"$border\" cellspacing=\"0\" class=\"allow\">\n<tr>\n<td>\n",
		"<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>",
		"</td>\n</tr>\n</table>\n<br>\n";
	}

	print "<a id=\"RES\"></a>";

	# �R�����g���p
	if ($refcom) {
		$refcom = "\n&gt; $refcom";
		$refcom =~ s/<br>/\r&gt; /g;
	}

	if (!$re_box) { $cref = 0; }
	if ($in{'refmode'} ne 'on') { $cref = 0; }
	require $formpl;
	&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$resub,$refcom,$csmail,$caikotoba,$cref,'reply');

	print <<EOM;
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���[�h����
#-------------------------------------------------
sub find {
	&header;
	print <<EOM;
<form action="$bbscgi">
EOM
	if ($in{'list'} ne "pickup") {
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
	}
	print <<EOM;
<input type="submit" value="&lt; �߂�">
</form>
<ul>
<li>�L�[���[�h����͂��A�u�����v�u�\\���v��I�����Č����{�^���������ĉ������B
<li>�L�[���[�h�̓X�y�[�X�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B
<p>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="find">
<input type="hidden" name="list" value="$in{'list'}">
�L�[���[�h <input type="text" name="word" size="35" value="$in{'word'}" class="f">
���� <select name="cond" class="f">
EOM

	if (!$in{'cond'}) { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected=\"selected\">$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}

	if (!$in{'view'}) { $in{'view'} = 10; }
	print qq|</select> �\\�� <select name="view" class="f">\n|;

	foreach (10,15,20,25) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected=\"selected\">$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}

	print <<EOM;
</select>
<input type="submit" value="����">
</form>
</ul>
EOM

	# �������s
	require $searchpl;
	if ($in{'word'} ne "") {
		($i,$next,$back) = &search($logfile,$in{'word'},$in{'view'},$in{'cond'});

		$enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$bbscgi?mode=find&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&list=$in{'list'}\">�O��$in{'view'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$bbscgi?mode=find&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&list=$in{'list'}\">����$in{'view'}��</a>]\n";
		}
	}

	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  ���e���
#-------------------------------------------------
sub form_disp {
	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

	# �N�b�L�[���擾
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	# �w�b�_���o��
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# �֘A�L���o��
	print <<EOM;
<form>
<input type="button" value="&lt; �߂�" onclick="history.back()">
</form>
���V�K���e�t�H�[��
<hr>
<a id="RES"></a>
EOM

	print "<form action=\"$registcgi\" method=\"$method\">\n";
	print <<EOM;
<!-- //
<input type="hidden" name="mode" value="write">
// -->
<input type="hidden" name="reno" value="$in{'no'}">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="refmode" value="$cref">
EOM

	if ($allowmode) {
		print "<table border=\"$border\" cellspacing=\"0\" class=\"allow\">\n<tr>\n<td>\n",
		"<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>",
		"</td>\n</tr>\n</table>\n<br>\n";
	}

	if (!$re_box) { $cref = 0; }
	require $formpl;
	&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,'',$inputform,$csmail,$caikotoba,$cref);

	print <<EOM;
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �J�E���^����
#-------------------------------------------------
sub counter {
	local($count, $cntup, @count);

	# �{�����̂݃J�E���g�A�b�v
	if ($mode eq '') { $cntup = 1; } else { $cntup = 0; }

	# �J�E���g�t�@�C����ǂ݂���
	open(LOG,"+< $cntfile") || &error("Open Error: $cntfile");
	eval "flock(LOG, 2);";
	$count = <LOG>;

	# IP�`�F�b�N�ƃ��O�j���`�F�b�N
	local($cnt, $ip) = split(/:/, $count);
	if ($addr eq $ip || $cnt eq "") { $cntup = 0; }

	# �J�E���g�A�b�v
	if ($cntup) {
		$cnt++;
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG "$cnt:$addr";
	}
	close(LOG);

	# ��������
	while(length($cnt) < $mini_fig) { $cnt = '0' . $cnt; }
	@count = split(//, $cnt);

	# GIF�J�E���^�\��
	if ($counter == 2) {
		foreach (0 .. $#count) {
			print "<img src=\"$gif_path/$count[$_]\.gif\" alt=\"$count[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}
	# �e�L�X�g�J�E���^�\��
	} else {
		print "<font color=\"$cntcol\" face=\"Verdana,Helvetica,Arial\">$cnt</font><br>\n";
	}
}

#-------------------------------------------------
#  �摜�C���[�W�\��
#-------------------------------------------------
sub image {
	my @ico1 = split(/\s+/, $ico1);
	my @ico2 = split(/\s+/, $ico2);

	&header;
	print <<EOM;
<div align="center">
<h4>�摜�C���[�W</h4>
<table border="$border" cellspacing="$cellspacing" cellpadding="10" class="thread" bgcolor="$tblcol">
EOM

	my $i = 0;
	foreach (0 .. $#ico1) {
		$i++;

		if ($i % 5 == 1) {
			print "<tr>\n";
		}
		print qq|<th><img src="$imgurl/$ico1[$_]" align="middle" alt="$ico1[$_]">$ico2[$_]</th>\n|;

		if ($i % 5 == 0) {
			print "</tr>\n";
		}
	}
	while ( $i % 5 != 0 ) {
		print qq|<td><br></td>|;
		$i++;
	}

	print <<EOM;
</table>
<br>
<form>
<input type="button" value=" ���� " onclick="top.close();">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �ړ��{�^��
#-------------------------------------------------
sub mvbtn {
	local($link,$i,$view) = @_;
	local($start,$end,$x,$y,$bk_bl,$fw_bl);

	if ($in{'bl'}) {
		$start = $in{'bl'}*10 + 1;
		$end   = $start + 9;
	} else {
		$in{'bl'} = 0;
		$start = 1;
		$end   = 10;
	}

	$x = 1; $y = 0;
	while ($i > 0) {
		# ���y�[�W
		if ($page == $y) {

			print qq {| <b style="color:red" class="n">$x</b>\n};

		# �ؑփy�[�W
		} elsif ($x >= $start && $x <= $end) {

			print "| <a href=\"$link$y&bl=$in{'bl'}&list=$in{'list'}\" class=n>$x</a>\n";

		# �O�u���b�N
		} elsif ($x == $start-1) {

			$bk_bl = $in{'bl'}-1;
			print "| <a href=\"$link$y&bl=$bk_bl&list=$in{'list'}\">��</a>\n";

		# ���u���b�N
		} elsif ($x == $end+1) {

			$fw_bl = $in{'bl'}+1;
			print "| <a href=\"$link$y&bl=$fw_bl&list=$in{'list'}\">��</a>\n";
		}

		$x++;
		$y += $view;
		$i -= $view;
	}

	print "|\n";
}

#-------------------------------------------------
#  URL�G���R�[�h
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  �^�C�g���ꗗ�\��
#-------------------------------------------------
sub SubjectList {
	my (%oyano,%oyasub,%date,%name,%tm,%new,$k);

	my $i = 0;
	my $j = 1;
	my @i = ();
	open(IN,"$logfile");
	my $top = <IN>;
	while (<IN>) {
		my ($no,$reno,$date,$name,$e,$sub,$m,$u,$h,$p,$c,$ic,$tm) = split(/<>/);
		if (!$reno) {
			$oyano{$j}  = $no;
			$oyasub{$j} = $sub;
			$i++;
			$j++;
		} else {
			$i[$j]++;
		}
		$date{$i} = $date;
		$name{$i} = $name;
		$tm{$i}   = $tm;
		$new{$i}  = $no;
	}
	close(IN);

	if ($j > $alltitle) {
		$j = $alltitle + 1;
	}

	if ($i) {
		print qq|<div align="center">\n|;
		print qq|<table border="0" bgcolor="$allt_col" width="90%" cellspacing="10" cellpadding="0" class="alltree">\n|;
		print qq|<tr><td>\n|;
	}

	for ($k = 1; $k < $j; $k++){
		my $co = sprintf("%01d",$i[$k+1]);
		print qq|<a href="$bbscgi?list=pickup&num=$oyano{$k}#$oyano{$k}">$k</a>:&nbsp;|;
		if ($newtitle) {
			print qq|<a href="$bbscgi?list=pickup&num=$oyano{$k}#$new{$k}" |;
		} else {
			print qq|<a href="$bbscgi?list=pickup&num=$oyano{$k}#$oyano{$k}" |;
		}
		print qq|title="�ŐV���e:$date{$k} (���e��:$name{$k})">$oyasub{$k}&nbsp;|;
		if ($co) {
			print qq|($co)</a>|;
		} else {
			print qq|</a>|;
		}
		# ���莞�Ԉȓ��̓��e��[NEW�}�[�N]�\��
		if (time - $tm{$k} < $new_time * 3600) {
			print qq|&nbsp;$newmark \n|;
		}
		print qq|&nbsp;<font color="$no_color">/</font>\n|;
	}
	print qq|</td></tr>\n</table>\n</div>\n|;
	if (!$boardmode) {
		print qq|<hr width="90%">\n|;
	}
}

#------------------------------------
#  Trap
#------------------------------------
sub wana {
	# IP�A�h���X�擾
	if (!$addr) { $addr = $ENV{'REMOTE_ADDR'}; }
	my $flag = 0;

	if(-e "$denyfile"){
		# �A�N�Z�X�����t�@�C��������
		open(IN, "$denyfile");
		eval { flock(IN, 1); };
		my $deny = <IN>;
		close (IN);
		# ���A�N�Z�X����IP�t�@�C���Ή�
		if ($deny =~ /\,/) { $deny =~ s/\,/\n/g;
			open (OUT,">$denyfile");
			eval { flock(OUT, 2); };
			print OUT "$deny\n";
			close OUT;
		}
		# �A�N�Z�X����IP������
		open(IN, "$denyfile");
		eval { flock(IN, 1); };
		my @denyip = <IN>;
		my @newip = @denyip;
		my $i = $#denyip;
		close (IN);
		foreach (@denyip) {
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
		if (!$flag) {
			# �V�K�̃A�N�Z�X����IP��ǉ�
			push(@newip,"$addr\n");
			while ($i >= $denynum) {
				# �Â��A�N�Z�X����IP���폜
				shift(@newip);
				$i--;
			}
			open (OUT,"+>$denyfile");
			eval { flock(OUT, 2); };
			print OUT @newip;
			close OUT;
		}
	} else {
		# �A�N�Z�X�����t�@�C����V���ɍ쐬
		open (OUT,">$denyfile");
		eval { flock(OUT, 2); };
		chmod (0606,"$denyfile");
		print OUT "$addr\n";
		close OUT;
		$flag = 1;
	}
	# Internal Server Error
	&cgi_error;
	exit;
}

__END__


