#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� admin.cgi - 2007/09/17
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
#�� YY-BOARD Antispam Version Modified by isso.
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

# �O���t�@�C���捞
require './init.cgi';
require $jcode;

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
$in{"$bbscheckmode"} = &decode_bbsmode($in{"$bbscheckmode"});

if ($mode eq "spam") { &spam; }
elsif ($mode eq "error") { &spam; }
elsif ($mode eq "spammsg") { &spammsg; }
elsif ($mode eq "spamclear") { &spamclear; }
elsif ($mode eq "spamdata") { &spamdata; }
elsif ($mode eq "editspam") { &editspam; }
elsif ($mode eq "sendmaillog") { &sendmaillog; }
elsif ($mode eq "maillogclear") { &maillogclear; }
elsif ($mode eq "admin_repost_form") { &admin_repost_form; }
elsif ($mode eq "reopen") { &reopen; }
elsif ($mode eq "set_cmode") { &set_cmode; }
elsif ($mode eq "cmode") { &save_cmode; }
elsif ($mode eq "chcolor") { &change_color; }
elsif ($mode eq "color_clear") { &color_clear; }
elsif ($mode eq "change_mode") { &change_mode; }
&admin;

#-------------------------------------------------
#  �Ǘ����[�h
#-------------------------------------------------
sub admin {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �y�[�W�J��z��
	foreach ( keys(%in) ) {
		if (/^page:(\d+)$/) {
			$page = $1;
			last;
		}
	}

	# �C�����
	if ($in{'job'} eq "edit" && $in{'no'}) {

		if ($in{'no'} =~ /\0/) { &error("�C���L���̑I���͂P�݂̂ł�"); }

		local($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm);

		open(IN,"$logfile") || &error("Open Error: $logfile");
		my $top = <IN>;
		while (<IN>) {
			chomp;
			($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);

			if ($no == $in{'no'}) { last; }
		}
		close(IN);

		# �Ǘ���
		my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
		if ($adminchk) {
			if ($cnam eq $admin_id && $cpwd eq $pass) {
				$nam = $admin_id;
				if($a_color) { $col = $a_color; }
			}
		}

		# �C���t�H�[��
		&edit_form($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm);

	# �C�����s
	} elsif ($in{'job'} eq "edit2" && $in{'no'}) {

		if ($in{'url'} eq "http://") { $in{'url'} = ''; }

		my @col = split(/\s+/, $color);
		my @ico1 = split(/\s+/, $ico1);
		if ($my_icon) { push(@ico1,$my_gif); }
		$in{'icon'} = $ico1[$in{'icon'}];

		# �Ǘ���
		if ($adminchk && $in{'name'} eq $admin_id) {
			@color = split(/\s+/, $color); $acol = $#color+1;
			$in{'color'} = $acol; $col[$acol] = $a_color;
			$in{'name'} = $a_name;
		}

		# URL���������N
		# if ($autolink) { $in{'comment'} = &auto_link($in{'comment'}); }

		my @new;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		my $top = <DAT>;
		while (<DAT>) {
			chomp;
			($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);

			if ($no == $in{'no'}) {
				$_ = "$no<>$re<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pw<>$col[$in{'color'}]<>$in{'icon'}<>$tm<>$in{'smail'}<>";
			}
			push(@new,"$_\n");
		}

		# �X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �폜
	} elsif ($in{'job'} eq "dele" && $in{'no'}) {

		my @del = split(/\0/, $in{'no'});

		# �폜�����}�b�`���O
		my @new;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		my $top = <DAT>;
		while (<DAT>) {
			my $flg;
			my ($no,$reno) = split(/<>/);

			foreach my $del (@del) {
				if ($no == $del || $reno == $del) {
					$flg = 1;
					last;
				}
			}
			if (!$flg) { push(@new,$_); }
		}

		# �X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		if ($keitai ne 'p') {
			&header;
			print <<EOM;
<a href="$bbscgi">�f���֖߂�</a>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="k_admin">
<input type="hidden" name="kmode" value="admin">
<input type="password" name="pass" size="8" value="$in{'pass'}">
<input type="submit" value=" �Ǘ����[�h " class="menu"></form>
</body>
</html>
EOM
		exit;
		}
	}

	&header;
	print <<EOM;
<div style="text-align: right;">
$ver <a href="http://swanbay-web.hp.infoseek.co.jp/index.html">Antispam Version</a></div>
<table border="0"><tr>
<td>
<form action="$bbscgi">
<input type="submit" value="�f���ɖ߂�" class="menu">
</form>
</td>
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="change_mode">
<input type="hidden" name="pass" value="$in{'pass'}">
EOM
	if ($boardmode) {
		print qq|<input type="hidden" name="boardmode" value="1">\n|;
		print qq|<input type="submit" value=" YY-BOARD�`���ɖ߂� " class="menu">\n|;
	} else {
		print qq|<input type="hidden" name="boardmode" value="0">\n|;
		print qq|<input type="submit" value=" �V�\\���`���ɕύX " class="menu">\n|;
	}
	print <<EOM;
</form>
</td>
EOM
	if ($boardmode) {
	print <<EOM;
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="set_cmode">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �J���[���[�h�ݒ� " class="menu">
</form>
</td>
EOM
	}


	# �f���ĊJ
	if ($clday) {
		my $last = (stat $logfile)[9];
		if (time - $last > $clday*24*3600) {
			print <<EOM;
<td>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="reopen">
<input type="submit" value="�f���ĊJ" class="menu">
</form>
</td>
EOM
		}
	}
	if(-s $er_log) {
		my $i = 0;
		open(IN,"$er_log");
		while (<IN>) {
			$i++;
		}
		close(IN);
		print <<EOM;
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="error">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="�G���[���O ($i��)" class="menu">
</form>
</td>
EOM
	}
	if (-e $spamdata) {
	print <<EOM;
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spamdata">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="NG���[�h�̈ꊇ�ҏW" class="menu">
</form>
</td>
EOM
	}

	if(-s $spamlogfile) {
		my $i = 0;
		open(IN,"$spamlogfile");
		while (<IN>) {
			$i++;
		}
		close(IN);
		print <<EOM;
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spam">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="$postmode ($i��)" class="menu">
</form>
</td>
EOM
	}

	if($webmail && (-e "$mailchk$sendmaillog")) {
	print <<EOM;
<td><form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="sendmaillog">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="���M�������{��" class="menu">
</form>
</td>
EOM
	}

	print <<EOM;
</tr>
</table>
<hr>
<ul>
<li>������I�����A�L�����`�F�b�N���đ��M�{�^���������ĉ������B</li>
<li>�e�L�����폜����ƃ��X�L�����ꊇ���č폜����܂��B</li>
</ul>
<form action="$admincgi" method="post">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="pass" value="$in{'pass'}">
�����F
<select name="job">
<option value="edit">�C��
<option value="dele">�폜
</select>
<input type="submit" value="���M����" class="post"><br>
<br>
EOM
	if ($boardmode) {
		print qq|<table width="100%" cellpadding="$cellpadding" cellspacing="$cellspacing" border="$border" class="thread">\n|;
		print qq|<tr>\n<td bgcolor="$tblcol">\n<br>\n|;
	} else { print qq|<dt><hr>|; }

	$pastView *= 2;

	my $i = 0; my $flg = 0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	my $top = <IN>;
	while (<IN>) {
		my ($no,$res,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col) = split(/<>/);

		if ($res eq "") { $i++; }
		if ($i < $page + 1) { next; }
		if ($i > $page + $pastView) { last; }

		if ($flg) {
			if (!$res) { print qq|<hr>\n|; }
		}
		if ($res eq "") { $flg = 1;}

		if ($eml) { $nam = "<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58$eml\">$nam</a>"; }
		($dat) = split(/\(/, $dat);

		$com =~ s/<[^>]*(>|$)//g;
		if (length($com) > 120) {
			$com = substr($com,0,120) . "...";
		}

		# �폜�`�F�b�N�{�b�N�X
		print qq|<dl>\n|;
		if ($res) { print qq|<dd>\n|; } else { print qq|&nbsp;|; }
		print qq|<input type="checkbox" name="no" value="$no">|;
		print qq|[<b>$no</b>] <b style="color:$subcol">$sub</b>\n|;
		print qq|���e�ҁF<b>$nam</b> ���e���F$dat &lt;<span style="color:$subcol">$hos</span>&gt;\n|;
		if ($res) { print qq|</dd>\n|; }
		print qq|<dd style="font-size:11px; color:$col;">$com</dd>\n|;
		print qq|</dl>\n|;
	}
	close(IN);
	if ($boardmode) { print qq|<br>\n</td>\n</tr>\n</table>\n</div>\n<br>\n|; }
	else { print qq|<dt><hr>\n</dl>|; }

	# �J��z���y�[�W
	my $next = $page + $pastView;
	my $back = $page - $pastView;

	if ($back >= 0) {
		print qq|<input type="submit" name="page:$back" value="�O��$pastView�g" class="post">\n|;
	}
	if ($next < $i) {
		print qq|<input type="submit" name="page:$next" value="����$pastView�g" class="post">\n|;
	}

	print <<EOM;
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub enter {
	&header;
	print <<EOM;
<blockquote>
<table border="0" cellspacing="0" cellpadding="26" width="400">
<tr><td align="center">
	<fieldset>
	<legend>
	���Ǘ��p�X���[�h����
	</legend>
	<form action="$admincgi" method="post">
	<input type="password" name="pass" size="16">
	<input type="submit" value=" �F�� " class="post">
	</form>
	</fieldset>
</td></tr>
</table>
</blockquote>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �C�����
#-------------------------------------------------
sub edit_form {
	local($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = @_;

	$com =~ s/<br>/\n/g;

	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }
	print <<EOM;
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; �O��ʂɖ߂�" class="post">
</form>
���ύX���镔���̂ݏC�����đ��M�{�^���������ĉ������B
<p>
<form action="$admincgi" method="post">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="job" value="edit2">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="no" value="$no">
EOM

	require $formpl;
	&form($nam,$eml,$url,'??',$ico,$col,$sub,$com,$sm);

	print <<EOM;
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �J���[���[�h�ݒ�
#-------------------------------------------------
sub set_cmode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	&header;
	print <<EOM;
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; �f����" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu /">
</form>
</td></tr>
</table></div>
<hr>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="cmode">
<input type="hidden" name="pass" value="$in{'pass'}">
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">�J���[���[�h��ύX���邱�Ƃ��ł��܂��B</td>
</tr>
<tr>
<td bgcolor="$tbl_col0">
<table border="$border" cellspacing="1" cellpadding="5">
<td bgcolor="$tblcol">
EOM

	open(COL,"$colorfile") || &error("�J���[���[�h�f�[�^�t�@�C�� $colorfile ������܂���B");
	$colormode = <COL>;
	close(COL);

	print "�J���[���[�h��&nbsp;<select name=colormode>\n";
	$selected0 = ""; $selected1 = ""; $selected2 = ""; $selected3 = ""; $selected4 = "";
	$selected5 = ""; $selected6 = ""; $selected7 = ""; $selected8 = ""; $selected9 = "";
	if    ($colormode eq "2") { $selected2 = "selected"; }
	elsif ($colormode eq "3") { $selected3 = "selected"; }
	elsif ($colormode eq "4") { $selected4 = "selected"; }
	elsif ($colormode eq "5") { $selected5 = "selected"; }
	elsif ($colormode eq "6") { $selected6 = "selected"; }
	elsif ($colormode eq "7") { $selected7 = "selected"; }
	elsif ($colormode eq "8") { $selected8 = "selected"; }
	elsif ($colormode eq "9") { $selected9 = "selected"; }
	else { $selected1 = "selected"; }
	print 
	"<option value=1 $selected1>�u���[�n",
	"<option value=2 $selected2>�s���N�n",
	"<option value=3 $selected3>�I�����W�n",
	"<option value=4 $selected4>�O���[���n",
	"<option value=5 $selected5>�C�G���[�n",
	"<option value=6 $selected6>���@�C�I���b�g�n",
	"<option value=7 $selected7>�z���C�g�n",
	"<option value=8 $selected8>�O���[�n",
	"<option value=9 $selected9>�u���b�N�n",
	"</select>&nbsp;��&nbsp;\n";

	print <<EOM;
<input type="submit" value="�ݒ肷��" class="post">
</td></tr></table>
</td></tr></table>
</form>
<br>
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">
�J���[���[�h��ύX��ɁA���L�̐ݒ��ݒ��ύX���邱�ƂŌf�����ڍׂɃJ�X�^�}�C�Y���邱�Ƃ��ł��܂��B
</td></tr>
<tr>
<td bgcolor="$tbl_col0">
<table border="$border" cellspacing="1" cellpadding="5">
<td bgcolor="$tblcol">
<table border="0">
<tr>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="chcolor">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="colormode" value="$colormode">
<td>�w�i�F</td><td><input type="text" name="bgcolor" size="8" value="$bgcolor"></td>
<td>�����F</td><td><input type="text" name="text" size="8" value="$text"></td>
<td>�J�E���^�F</td><td><input type="text" name="cntCol" size="8" value="$cntcol"></td>
<td>�^�C�g�������F</td><td><input type="text" name="tCol" size="8" value="$tCol"></td>
</tr><tr>
<td>�L���\\�����̉��n�F</td><td><input type="text" name="tblCol" size="8" value="$tblcol"></td>
<td>�e�L�����w�i�F</td><td><input type="text" name="tbl_col0" size="8" value="$tbl_col0"></td>
<td>�X���b�h�g�T�C�Y</td><td><input type="text" name="thr_brd" size="8" value="$thr_brd"></td>
<td>�X���b�h�S�̕�</td><td><input type="text" name="width" size="8" value="$width"></td>
</tr><tr>
<td>���e�t�H�[���w�i�F</td><td><input type="text" name="frm_bc" size="8" value="$frm_bc"></td>
<td>���e�t�H�[�������F</td><td><input type="text" name="frm_tx" size="8" value="$frm_tx"></td>
<td>���e�t�H�[���g�F</td><td><input type="text" name="frm_brd" size="8" value="$frm_brd"></td>
<td>���e�t�H�[���g�T�C�Y</td><td><input type="text" name="frm_solid" size="8" value="$frm_solid"></td>
</tr><tr>
<td>�{�^�������F</td><td><input type="text" name="btx_col" size="8" value="$btx_col"></td>
<td>�{�^���g�F</td><td><input type="text" name="btn_solid" size="8" value="$btn_solid"></td>
<td>���j���[�����F</td><td><input type="text" name="menu_chr" size="8" value="$menu_chr"></td>
<td>���j���[�w�i�F</td><td><input type="text" name="menu_bg" size="8" value="$menu_bg"></td>
</tr><tr>
<td>���j���[�g�F</td><td><input type="text" name="menu_solid" size="8" value="$menu_solid"></td>
<td>���j���[�g�T�C�Y</td><td><input type="text" name="menu_brd" size="8" value="$menu_brd"></td>
<td>�^�C�g���ꗗ�w�i�F</td><td><input type="text" name="allt_col" size="8" value="$allt_col"></td>
<td>�^�C�g���ꗗ�g�F</td><td><input type="text" name="allt_solid" size="8" value="$allt_solid"></td>
</tr><tr>
<td>�^�C�g���ꗗ�g�T�C�Y</td><td><input type="text" name="allt_brd" size="8" value="$allt_brd"></td>
<td>�R�����g���w�i�F</td><td><input type="text" name="tbl_col1" size="8" value="$tbl_col1"></td>
<td>�e�L�X�g�G���A�g�T�C�Y</td><td><input type="text" name="tarea_brd" size="8" value="$tarea_brd"></td>
<td>���͗��g�T�C�Y</td><td><input type="text" name="btn_brd" size="8" value="$btn_brd"></td>
</tr><tr>
<td>���e�t�H�[�����n�F</td><td><input type="text" name="formCol1" size="8" value="$formCol1"></td>
<td>���e�t�H�[�������F</td><td><input type="text" name="formCol2" size="8" value="$formCol2"></td>
<td>���e�{�^�������F</td><td><input type="text" name="post_chr" size="8" value="$post_chr"></td>
<td>���e�{�^���w�i�F</td><td><input type="text" name="post_bg" size="8" value="$post_bg"></td>
</tr><tr>
<td>���e�{�^���g�F</td><td><input type="text" name="post_solid" size="8" value="$post_solid"></td>
<td>���e�{�^���g�T�C�Y</td><td><input type="text" name="post_brd" size="8" value="$post_brd"></td>
<td>���e�L�[�摜�̕����F</td><td><input type="text" name="moji_col" size="8" value="$moji_col"></td>
<td>���e�L�[�摜�̔w�i�F</td><td><input type="text" name="back_col" size="8" value="$back_col"></td>
</tr><tr>
<td>���W�I�{�^���g�T�C�Y</td><td><input type="text" name="radio_brd" size="8" value="$radio_brd"></td>
<td>�X���b�h�S�̘g��</td><td><input type="text" name="border" size="8" value="$border"></td>
<td>�X���b�h�g��</td><td><input type="text" name="cellspacing" size="8" value="$cellspacing"></td>
<td>�X���b�h�g�]��</td><td><input type="text" name="cellpadding" size="8" value="$cellpadding"></td>
</tr><tr>
<td>�e�L���}�[�N</td><td><input type="text" name="topmark" size="8" value="$topmark"></td>
<td>�R�����g�}�[�N</td><td><input type="text" name="comark" size="8" value="$comark"></td>
<td>�R�����g�����}�[�W��</td><td><input type="text" name="margin_left" size="8" value="$margin_left"></td>
<td>�R�����g���E�}�[�W��</td><td><input type="text" name="margin_right" size="8" value="$margin_right"></td>
</tr><tr>
<td>�L�� [�^�C�g��] �F</td><td><input type="text" name="subCol" size="8" value="$subcol"></td>
<td>�L�� [�^�C�g��] ������</td><td><input type="text" name="sub_len" size="8" value="$sub_len"></td>
<td>���p�������F</td><td><input type="text" name="refcol" size="8" value="$refcol"></td>
<td>�c���[�I���L���w�i�F</td><td><input type="text" name="tree_bc" size="8" value="$tree_bc"></td>
</tr><tr>
<td>�{�^���w�i�F</td><td><input type="text" name="btn_col" size="8" value="$btn_col"></td>
<td>���b�Z�[�W�s�Ԋu</td><td><input type="text" name="lheight" size="8" value="$lheight"></td>
EOM
	print "<td>�w�i�摜��</td><td><select name=\"scroll\">\n";
	$selected0 = ""; $selected1 = "";
	if ($scroll eq "1") { $selected1 = "selected";
	} else { $selected0 = "selected"; }
	print "<option value=\"0\" $selected0>�X�N���[������",
	"<option value=\"1\" $selected1>�Œ肷��",
	"</select></td>\n";

	print "<td>���b�Z�[�W���w�i�摜��</td><td><select name=\"thr_bg\">\n";
	$selected0 = ""; $selected1 = "";
	if ($thr_bg eq "1") { $selected1 = "selected";
	} else { $selected0 = "selected"; }
	print "<option value=\"0\" $selected0>���߂��Ȃ�",
	"<option value=\"1\" $selected1>���߂���",
	"</select></td>\n";
	print <<EOM;
</tr><tr>
<td>
<br>
<input type="submit" value="�ݒ�ύX����" class="post">
</td>
</tr>
</table>
</td></tr></table>
</td></tr></table>
</form>
<br>
<br>
<p>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="color_clear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="�ݒ������������" class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �J���[���[�h�ۑ�
#-------------------------------------------------
sub save_cmode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	open(OUT,">$colorfile") || &error("�J���[�f�[�^�t�@�C�� $colorfile �𐳂����X�V�ł��܂���ł����B");
	print OUT "$in{'colormode'}";
	close(OUT);

	# �\�����[�h�ݒ�
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  �J���[���[�h�ݒ�ύX
#-------------------------------------------------
sub change_color {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	open(PARA,"$colordata") || &error("�J���[�f�[�^�t�@�C�� $colordata ������܂���B");
	@para = <PARA>;
	close(PARA);

	$para[$in{'colormode'}] = "$in{'bgcolor'}<>$in{'text'}<>$in{'cntCol'}<>$in{'tCol'}<>$in{'tblCol'}<>$in{'tbl_col0'}<>$in{'thr_brd'}<>$in{'menu_chr'}<>$in{'menu_bg'}<>$in{'menu_solid'}<>$in{'menu_brd'}<>$in{'allt_col'}<>$in{'allt_solid'}<>$in{'allt_brd'}<>$in{'tbl_col1'}<>$in{'tarea_brd'}<>$in{'btn_col'}<>$in{'btx_col'}<>$in{'btn_solid'}<>$in{'btn_brd'}<>$in{'formCol1'}<>$in{'formCol2'}<>$in{'post_chr'}<>$in{'post_bg'}<>$in{'post_solid'}<>$in{'post_brd'}<>$in{'moji_col'}<>$in{'back_col'}<>$in{'radio_brd'}<>$in{'border'}<>$in{'cellspacing'}<>$in{'cellpadding'}<>$in{'topmark'}<>$in{'comark'}<>$in{'margin_left'}<>$in{'margin_right'}<>$in{'subCol'}<>$in{'sub_len'}<>$in{'frm_brd'}<>$in{'frm_bc'}<>$in{'frm_tx'}<>$in{'frm_solid'}<>$in{'refcol'}<>$in{'tree_bc'}<>$in{'scroll'}<>$in{'thr_bg'}<>$in{'lheight'}<>$in{'width'}<>\n";


	# �ݒ�t�@�C����ۑ�
	open(OUT,">$colordata") || &error("�J���[�f�[�^�t�@�C�� $colordata �𐳂����X�V�ł��܂���ł����B");
	print OUT @para;
	close(OUT);

	# �\�����[�h�ݒ�
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  �J���[���[�h�ݒ菉����
#-------------------------------------------------
sub color_clear {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	unlink("$colordata");
	rename($colorinit,$colordata) || &error("�J���[�ݒ�t�@�C���G���[");

	open(PARA,"$colordata");
	@para = <PARA>;
	close(PARA);

	open(COL,">$colorinit");
	print COL @para;
	close(COL);

	open(OUT,">$colorfile");
	print OUT "1";
	close(OUT);

	# �\�����[�h�ݒ�
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  �\���`���ύX
#-------------------------------------------------
sub change_mode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	if ($in{'boardmode'}) {
		open(OUT,">$colorfile");
		print OUT "0";
		close(OUT);
	} else {
		open(OUT,">$colorfile");
		print OUT "1";
		close(OUT);
	}

	# �\�����[�h�ݒ�
	&message("�\\�����[�h��ύX���܂���");
}

#-------------------------------------------------
#  �f���ĊJ
#-------------------------------------------------
sub reopen {
	my @data = ();
	# ���O�ǂݍ���
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		push(@data,"$_");
	}

	# �X�V
	seek(DAT, 0, 0);
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	&message("�f�����ĊJ���܂���");
}

#-------------------------------------------------
#  �X�p�����O
#-------------------------------------------------
sub spam {
	my (%reno,%date,%name,%email,%sub,%url,%msg,%host,%pwd,%color,
	%icon,%sml,%reason,%tim,%pdate,%timecheck,%useragent,%fcheck);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	my $file = $spamlogfile;
	my $job = "spam";
	if ($mode eq "error") {
		$job = "error";
		$file = $er_log;
		$postmode = "�G���[";
		$alreason = "�G���[���R";
	}

	&header;
	print <<EOM;
<ul>
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; �f����" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
</td></tr>
</table></div>
</ul>
<ul><li>$postmode���O<br>
�K�p��$postmode�𕜊����������Ƃ́A�u$postmode���O���폜�v���Ă����ĉ������B
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spamclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job"  value="$job">
<input type="submit" value=" $postmode���O��S�č폜���� " class="post">
</form>
EOM
	open(IN,"$file");
	eval { flock(IN, 1); };
	my $i = 0;
	while (<IN>) {
		my ($no,$reno,$date,$name,$email,$sub,$msg,$url,$host,$pwd,$color,
		$icon,$tim,$sml,$reason,$fcheck,$referer,$useragent) = split(/<>/);
		$reno{$i}      = $reno;
		$date{$i}      = $date;
		$name{$i}      = $name;
		$email{$i}     = $email;
		$sub{$i}       = $sub;
		$url{$i}       = $url;
		$msg{$i}       = $msg;
		$host{$i}      = $host;
		$pwd{$i}       = $pwd;
		$color{$i}     = $color;
		$icon{$i}      = $icon;
		$sml{$i}       = $sml;
		$reason{$i}    = $reason;
		$tim{$i}       = $tim;
		$pdate{$i}     = &get_time($tim);
		$timecheck{$i} = &encode_bbsmode($fcheck);
		$useragent{$i} = &escape($useragent);
		if ($fcheck) {
			$fcheck{$i} = &get_time($fcheck);
		} else {
			$fcheck{$i} = qq|�A�N�Z�X�L�^�Ȃ�|;
		}
		if ($keychange) {
			if ($url{$i} && $url{$i} =~ /\@/) {
				($email{$i},$url{$i}) = ($url{$i},$email{$i});
			} elsif ($email{$i} && $email{$i} !~ /\@/) {
				($email{$i},$url{$i}) = ($url{$i},$email{$i});
			}
		}
		$i++;
	}
	close(IN);

	# �\�[�g����
	my $j = 0;
	my $x = 0;
	my $page = $in{'page'};
	foreach (sort { ($date{$b} cmp $date{$a}) } keys(%date)) {
		$j++;
		if ($j < $page + 1) { next; }
		if ($j > $page + $spamlog_page) { next; }

		$useragent = "<small>$useragents</small>";
		print "<p><table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n",
			"<tr bgcolor=\"$tbl_col0\">\n<td bgcolor=\"$tbl_col0\">";
		print "<table border=\"$border\" cellspacing=\"1\" cellpadding=\"5\">\n";
		print "<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">���e����</td><td bgcolor=\"$tblcol\">$pdate{$_}</td>",
			"<td bgcolor=\"$tblcol\">�^�C�g��</td><td bgcolor=\"$tblcol\">$sub{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">�A�N�Z�X����</td><td bgcolor=\"$tblcol\">$fcheck{$_}</td>",
			"<td bgcolor=\"$tblcol\">$alreason</td><td bgcolor=\"$tblcol\">$reason{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">���e�Җ�</td><td bgcolor=\"$tblcol\">$name{$_}</td>",
			"<td bgcolor=\"$tblcol\">URL</td><td bgcolor=\"$tblcol\">$url{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">�z�X�g�A�h���X</td><td bgcolor=\"$tblcol\">$host{$_}</td>",
			"<td bgcolor=\"$tblcol\">�u���E�U</td><td bgcolor=\"$tblcol\">$useragent{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
		"<td bgcolor=\"$tblcol\">���[���A�h���X</td><td bgcolor=\"$tblcol\">$email{$_}</td>",
		"<td bgcolor=\"$tblcol\">���e���e</td><td bgcolor=\"$tblcol\"> ";
		if ($msg{$_}) {
			print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spammsg">
<input type="hidden" name="job"  value="$job">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="msg" value="$msg{$_}">
<input type="submit" value="���e���e���{��" class="post">
</form>
EOM
		} else {
			print qq|<div align="center"> - </div>|;
		}
		print <<EOM;
</td></tr></table>
</td></tr></table>
<table border="0"><tr><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin_repost_form">
<input type="hidden" name="job"  value="$job">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="reno"  value="$reno{$_}">
<input type="hidden" name="date"  value="$date{$_}">
<input type="hidden" name="name"  value="$name{$_}">
<input type="hidden" name="email" value="$email{$_}">
<input type="hidden" name="sub"   value="$sub{$_}">
<input type="hidden" name="msg"   value="$msg{$_}">
<input type="hidden" name="url"   value="$url{$_}">
<input type="hidden" name="host"  value="$host{$_}">
<input type="hidden" name="pwd"   value="$pwd{$_}">
<input type="hidden" name="color" value="$color{$_}">
<input type="hidden" name="icon"  value="$icon{$_}">
<input type="hidden" name="sml"   value="$sml{$_}">
<input type="hidden" name="tim"   value="$tim{$_}">
<input type="hidden" name="$bbscheckmode" value="$timecheck{$_}">
<input type="hidden" name="reason" value="$reason{$_}">
<input type="submit" value="�ē��e����" class="post">
</form></td><td>(��L�̓��e�𕜊������邱�Ƃ��ł��܂�)</td></tr></table>
EOM
	}

	print "</table><br>\n";
	my $next = $page + $spamlog_page;
	my $back = $page - $spamlog_page;

	print "<table><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$admincgi\" method=\"$method\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"$in{'mode'}\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$back\">\n";
		print "<input type=\"submit\" value=\"�O���\"></form></td>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$admincgi\" method=\"$method\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"$in{'mode'}\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$next\">\n";
		print "<input type=\"submit\" value=\"�����\"></form></td>\n";
	}
	print "</tr></table>\n";
	print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spamclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job"  value="$job">
<input type="submit" value=" $postmode���O��S�č폜���� " class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���e���ۃ��O������
#-------------------------------------------------
sub spamclear {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	my $file = $spamlogfile;
	if ($in{'job'} eq "error") {
		$file = $er_log;
		$postmode = "�G���[";
	}

	# ���e���ۃ��O�̏�����
	open(CL,"+>$file");
	close(CL);

	&header();
	print <<EOM;
<div align="center">
<h4>$postmode���O���폜���܂���</h4>
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; �f����" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
</td></tr>
</table></div>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���e���ۃR�����g
#-------------------------------------------------
sub spammsg {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	if ($in{'job'} eq "error") {
		$postmode = "�G���[";
	}

	# �G�X�P�[�v
	$in{'msg'} =~ s/"/&quot;/g;
	$in{'msg'} =~ s/</&lt;/g;
	$in{'msg'} =~ s/>/&gt;/g;
	# ���s����
	$in{'msg'} =~ s/&lt;br&gt;/<br>/ig;

	&header();
	print <<EOM;
<div align="center">
<h4>�R�����g</h4>
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">
<table border="$border" cellspacing="1" cellpadding="5">
<tr bgcolor="$tblcol">
<td bgcolor="$tblcol"><div align="center">
$postmode ���b�Z�[�W���e</div></td></tr>
<tr bgcolor="$tblcol">
<td bgcolor="$tblcol">$in{'msg'}</td></tr>
</table>
</td></tr>
</table><br>
<table border="0">
<tr><td><form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="$in{'job'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" $postmode���O�{���ɖ߂� " class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
</td></tr>
</table></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  NG���[�h�ҏW
#-------------------------------------------------
sub spamdata {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	&header;
	print <<EOM;
<div align="left">
<table border="0">
<tr><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
</td></tr>
</table></div>
<br>
<li>NG���[�h���ꊇ�o�^�ł��܂�(���p�̃J���}�ŋ�؂�)�B<br>
<br>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="editspam">
<input type="hidden" name="pass" value="$in{'pass'}">
EOM
	if (-e $spamdata) {
		open(IN,"$spamdata");
		$SPMLST = <IN>;
		close(IN);
	}

	print <<EOM;
<textarea name="SPMLST" rows="30" cols="80" wrap="soft">$SPMLST</textarea><br>
<br>
<input type="submit" value="�X�V����" class="post">
</form>
</ul>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  NG���[�h�X�V
#-------------------------------------------------
sub editspam {

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	$SPMLST = $in{"SPMLST"};

	# ��f�[�^�E���s�E�󔒂��폜
	$SPMLST =~ s/�C/\,/g;
	$SPMLST =~ s/<br>//ig;
	$SPMLST =~ s/<br>//ig;
	$SPMLST =~ s/\n//g;
	$SPMLST =~ s/\r//g;
	$SPMLST =~ s/�@//g;
	$SPMLST =~ s/\,{2,}/\,/g;
	$SPMLST =~ s/^\,{1,}//;

	open(OUT,">$spamdata") || &error("Write Error");
	print OUT $SPMLST;
	close(OUT);

	&header;

	print <<EOM;
<div align="center">
<h4>NG���[�h���X�V���܂���</h4>
<br>
<table border="0">
<tr><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
</td></tr>
</table></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �Ǘ��ҍē��e���
#-------------------------------------------------
sub admin_repost_form {

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	if ($in{'job'} eq "error") {
		$postmode = "�G���[";
		$alreason = "�G���[���R";
	}

	$in{'msg'} =~ s/<br>/\n/g;
	$in{'msg'} =~ s/&lt;br&gt;/\n/g;
	$in{"$bbscheckmode"} = &encode_bbsmode($in{"$bbscheckmode"});

	local($cflag) = 0;
	local($j) = 0;
	foreach(split(/\s+/, $color)) {
		if ($in{'color'} =~ /\Q$_\E/) {
			$cflag = 1; $col = $j; last;
		}
		$j++;
	}
	if(!$cflag) { $col = 0; }

	&header;
	print <<EOM;
<h3>$postmode�Ƃ��ď������ꂽ���L�̓��e�𕜊������܂��B</h3>
<hr>
<table border="0" cellspacing="1">
<form action="$registcgi" method="$method">
<input type="hidden" name="$bbscheckmode" value="$in{$bbscheckmode}">
<input type="hidden" name="mode" value="admin_repost">
<input type="hidden" name="job"  value="$in{'job'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="reno" value="$in{'reno'}">
<input type="hidden" name="date" value="$in{'date'}">
<input type="hidden" name="host" value="$in{'host'}">
<input type="hidden" name="pwd" value="$in{'pwd'}">
<input type="hidden" name="color" value="$col">
<input type="hidden" name="icon" value="$in{'icon'}">
<input type="hidden" name="smail" value="$in{'sml'}">
<input type="hidden" name="tim" value="$in{'tim'}">
<tr>
  <td><b style='color:#FF0000'>$alreason&nbsp;:&nbsp;$in{'reason'}</b><br><br></td>
</tr>
<tr>
  <td><b>�����O</b>&nbsp;:&nbsp;
    <input type="text" name="name" value="$in{'name'}" size="28" class="f"></td>
</tr>
<tr>
  <td><b>�d���[��</b>&nbsp;:&nbsp;
    <input type="text" name="email" size="36" value="$in{'email'}"></td>
</tr>
<tr>
  <td><b>�t�q�k</b>&nbsp;:&nbsp;
  <input type="text" name="url" size="50" value="$in{'url'}" class="f"></td>
</tr>
<tr>
  <td><b>�^�C�g��</b>&nbsp;:&nbsp;
    <input type="text" name="sub" size="36" value="$in{'sub'}" class="f">
  </td>
</tr>
<tr>
  <td>
    <b>���b�Z�[�W</b><br>
    <textarea cols="56" rows="7" name="comment" wrap="soft" class="f">$in{'msg'}</textarea>
  </td>
</tr>
</table>
<table><tr><td>
<input type="submit" value="���e������������" class="post">
</form>
</td>
<form action="$admincgi" method="$method">
<td><input type="hidden" name="mode" value="$in{'job'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" $postmode���O�{���ɖ߂� " class="post">
</form>
</td></tr></table>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  Webmail���M���O
#-------------------------------------------------
sub sendmaillog {
	my (%dat,%nam,%em,%to,%sem,%hos,%no,%date);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	&header;
	print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ���ʂɖ߂� " class="menu">
</form>
<li>Webmail���M���O
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="maillogclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" ���M�L�^���폜���� " class="post">
</form>
<p>Webmail�𗘗p�������[�����M�L�^�ł��B</p>
<table border="1">\n<tr><td>����</td><td>���M�Җ�</td><td>���M�҃��[���A�h���X</td>
<td>���M���z�X�g�A�h���X</td><td>��M�Җ�</td><td>��M�҃��[���A�h���X</td><td>�L��No</td></tr>
EOM

	if(-e "$mailchk$sendmaillog") {
		open(IN,"$mailchk$sendmaillog") || &error("Open Error : $mailchk$sendmaillog");
		my $i = 0;
		while (<IN>) {
			my ($dat,$nam,$em,$to,$sem,$hos,$no) = split(/<>/);
			$dat{$i} = $dat;
			$nam{$i} = $nam;
			$em{$i}  = $em;
			$to{$i}  = $to;
			$sem{$i} = $sem;
			$hos{$i} = $hos;
			$no{$i}  = $no;
			$date{$i} = &get_time($dat{$i});
			$i++;
		}
		close(IN);

		foreach (sort { ($dat{$b} cmp $dat{$a}) } keys(%dat)) {
			print "<tr><td><small>$date{$_}</small></td><td>$nam{$_}</td><td>$em{$_}</td>",
			"<td>$hos{$_}</td><td>$to{$_}</td><td>$sem{$_}</td><td>$no{$_}</td></tr>";
		}
	}
	print <<EOM;
</table><br>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="maillogclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" ���M�L�^���폜���� " class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���M�L�^���폜
#-------------------------------------------------
sub maillogclear {
	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	unlink("$mailchk$sendmaillog");

	&header;
	print <<EOM;
<li>Webmail���M���O���폜���܂����B</li>
<br>
<br>
<table><tr><td>
<form action="$bbscgi" method="$method">
<input type="hidden" name="page" value="$page">
<input type="submit" value="&lt; �f����" class="menu">
</form>
</td>
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" �Ǘ����[�h�ɖ߂� " class="menu">
</form>
</tr></table>
</body>
</html>
EOM
	exit;
}


__END__


