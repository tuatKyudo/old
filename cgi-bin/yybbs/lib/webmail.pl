#����������������������������������������������������������������������
#�� webmail.pl for YY-BOARD ver 2.00
#�� Copyright isso. April, 2008
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#����������������������������������������������������������������������

#-------------------------------------------------
#  ���[���쐬�t�H�[��
#-------------------------------------------------
sub writemail {
	# ���t�@���[�`�F�b�N
	if (!$ENV{'HTTP_REFERER'}) {
		if ($referercheck != 2) {
			&error("���[�����M�t�H�[���ւ͒��ڃA�N�Z�X�ł��܂���B");
		} else {
			# Internal Server Error
			&cgi_error;
		}
	}

	# �A�����M�`�F�b�N
	my $flg = 0;
	if (-s "$mailchk$sendmaillog") {
		open(DAT,"$mailchk$sendmaillog");
		eval { flock(DAT, 1); };
		my $top = <DAT>;
		close(DAT);
		my ($t,$a,$e,$o,$s,$h,$n) = split(/<>/, $top);
		if (abs(time - $t) < $errtime) {
			if ($host eq $h || $in{'no'} eq $n) {
				$flg = 1;
			}
		}
		# �A�����M
		if ($flg) {
			&error("�A�����M�͂ł��܂���B");
		}
	}

	my ($s_name, $s_email, $s_smail, $s_msg, $s_sub, $s_no);
	# �N�b�L�[���擾
	my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	open(IN,"$logfile") || &error("���O�t�@�C�� $logfile ������܂���B");
	my $top = <IN>;
	eval { flock(IN, 1); };
	while (<IN>) {
		chomp;
		my ($no,$r,$d,$nam,$eml,$sub,$com,$u,$h,$p,$c,$i,$t,$sml) = split(/<>/);
		if ($in{'no'} == $no) {
			$s_name  = $nam;
			$s_email = $eml;
			$s_smail = $sml;
			$s_msg   = $com;
			$s_sub   = $sub;
			$s_no    = $no;
		}
	}
	close(IN);

	if (!$webmail || $s_smail ne "1" || $s_email eq "") { &error("�s���ȃA�N�Z�X�ł��B"); }

	# �R�����g���b�Z�[�W
	my $res_msg = "\n\> $s_msg";
	$res_msg =~ s/&amp;/&/g;
	$res_msg =~ s/<br>/\r> /g;

	# �R�����g�^�C�g��
	my $res_sub = $s_sub;
	$res_sub =~ s/<([^>]|\n)*>//g;

	# sendmail�`�F�b�N
	if (-d $mailchk) {
		open(OUT,">$mailchk$host") || &error("���M�ł��܂���B�Ǘ��҂ɂ��₢���킹�������B");
		eval { flock(OUT, 2); };
		print OUT $host;
		close(OUT);
	} else {
		mkdir ($mailchk, 0707) || &error("���M�ł��܂���B�Ǘ��҂ɂ��₢���킹�������B");
		open(OUT,">$mailchk$host");
		eval { flock(OUT, 2); };
		print OUT $host;
		close(OUT);
	}

	# HTML���o��
	&header;

	# �_�~�[
	&pseudo;

	my $access = &encode_bbsmode();
	my $enaddress = &encode_addr();
	if ($keychange) {
		$url_key  = 'email'; $mail_key = 'url'; $name_key = 'comment'; $comment_key = 'name';
	} else {
		$url_key  = 'url'; $mail_key = 'email'; $name_key = 'name'; $comment_key = 'comment';
	}

	print <<EOM;
<div style="text-align: left;">
<form>
<input type="button" value="&lt;&lt; �߂�" onclick="history.back()">
<input type="hidden" name="list" value="$in{'list'}">
</form>
</div>
<div style="text-align: center;">
<hr width="500">
<h3>���L�̓��e�œ��e�� $s_name ����Ƀ��[���𑗐M���܂��B</h3>
�Ȃ��A�������烁�[���h�~�̂��߁A���[���{���ȊO�̑��M�����L�^���Ă���܂��B
<hr width="500">
<br>
EOM
	if ($boardmode) {
		print qq|<table width="90%" border="0" cellpadding="$cellpadding">\n<tr><td>\n|;
		print qq|<br>\n|;
	}
	print <<EOM;
<form action="$bbscgi?" method="$method">
<input type="hidden" name="$bbscheckmode" value="$access">
<!-- //
<input type="hidden" name="mode" value="write">
// -->
<input type="hidden" name="no" value="$s_no">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="act" value="$in{'act'}">
<table border="0" cellspacing="0" cellpadding="1" style="margin-left: auto; margin-right: auto;">
<tr class="topdisp">
  <td nowrap>Subject</td>
  <td>
    <input type="text" name="subject" size="36" value="">
    <b style="color:#ff0000;">���͋֎~</b>
  </td>
</tr>
<tr class="topdisp">
  <td nowrap>Title</td>
  <td>
    <input type="text" name="title" size="36" value="">
    <b style="color:#ff0000;">���͋֎~</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>�^�C�g��</b></td>
  <td>
    <input type="text" name="sub" size="36" value="$res_sub">
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>���Ȃ܂�</b></td>
  <td><input type="text" name="$name_key" size="36" value="$cnam"><b style="color:#ff0000;">���K�{</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>�d���[��</b></td>
  <td>
    <input type="hidden" name="mail" size="28" value="$enaddress">
    <input type="text" name="$mail_key" size="36" value="$ceml"><b style="color:#ff0000;">���K�{</b>
  </td>
</tr>
<tr class="topdisp">
  <td nowrap><b style="color:#ff0000;">���͋֎~</b></td>
  <td>
    <input type="text" name="$url_key" size="10" value="">
  </td>
</tr>
EOM
	print qq|<tr>  <td nowrap |;
	if (!$boardmode) {
		print qq|colspan="2" |;
	}
	print qq|class="form"><b>���b�Z�[�W</b>|;
	if ($boardmode) {
		print qq|  </td>\n  <td>\n|;
	} else {
		print qq|<br>\n|;
	}
	print <<EOM;
    <textarea name="$comment_key" rows="14" cols="70" wrap="soft">$res_msg</textarea>
  </td>
</tr>
<tr>
  <td colspan="2">
    <script type="text/javascript">
    <!-- //
    fcheck("name='mode' value","<input t","ype='hidden' ","='sendmail'>");
    fcheck("value='���M����'><input t","<input t","ype='submit' name='submit' ","ype='reset' value='���Z�b�g'>");
    // -->
    </script>
    <noscript><br><b>Javascript�������Ȃ��ߑ��M�ł��܂���B</b><br><br></noscript>
  </td>
</tr>
</table></form>
</div>
EOM
	if ($boardmode) {
		print qq|</td></tr>\n</table>\n|;
	}
	print <<EOM;
</body>
</html>
EOM
	exit;

}

#-------------------------------------------------
#  ���[�����M���[�`��
#-------------------------------------------------
sub sendmail {
	$spammail = 0;
	my ($s_smail,$s_email,$s_name);

	# POST����
	if ($MethPost && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	open(IN,"$logfile") || &error("���O�t�@�C�� $logfile ������܂���B");
	my $top = <IN>;
	eval { flock(IN, 1); };
	while (<IN>) {
		chomp;
		my ($no,$r,$d,$nam,$eml,$sub,$com,$u,$h,$p,$c,$i,$t,$sml) = split(/<>/);
		if ($in{'no'} == $no) {
			$s_email = $eml;
			$s_smail = $sml;
			$s_name  = $nam;
		}
	}
	close(IN);

	if (!$webmail || $s_smail ne "1" || $s_email eq "") {
		&error("���M�ł��܂���B","1");
	}

	if ($in{'email'} eq "" || $in{'name'} eq "") {
		&error("�d���[���Ƃ��Ȃ܂��̓��͕͂K�{�ł��B","1");
	}

	# �d���[������
	if ($in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,3}/) {
		&error("�d���[���̓��͂��s���ł�","1");
	}
	my $atmark = $in{'email'} =~ s/\@/\@/g;
	if ($atmark != 1) {
		&error("�d���[���̓��͂��s���ł�","1");
	}

	# �X�p�����M�΍�
	my $acctime = &decode_bbsmode($in{"$bbscheckmode"});
	my $enadr = &encode_addr($addr);
	if($ipcheckmode) {
		if ($in{'mail'} ne $enadr) {
			&error("�ڑ��z�X�g��񂪕s���Ȃ��ߑ��M�ł��܂���ł����B","1");
		}
	} else {
		if ($in{'mail'} =~ /\@/) {
			&error("���͓��e���s���Ȃ��ߑ��M�ł��܂���ł����B","1");
		}
	}

	my $tcheck = abs(time - $acctime);
	if ($tcheck < $mintime || $tcheck > $maxtime) {
		&error("�s���ȑ��M�͋֎~����Ă��܂��B","1");
	}

	if ($in{'submit'} ne "���M����") {
		&error("����Ƀ��[���𑗐M�ł��܂���ł����B","1");
	}

	if ($in{'url'} || $in{'subject'} || $in{'title'} || $in{'name'} =~ /https?\:\/\//i) {
		&error("���͓��e���s���Ȃ��ߑ��M�ł��܂���ł����B","1");
	}

	if (length($in{'comment'}) < length($in{'name'})) {
		&error("���b�Z�[�W���Z�����邽�ߑ��M�ł��܂���ł����B","1");
	}

	if ($japanese) {
		if ($in{'comment'} !~ /(\x82[\x9F-\xF2])/) {
			&error("���{��ł̓��͂��K�{�ł��B(Japanese Only)","1");
		}
	}

	if (-e "$mailchk$host") {
		unlink("$mailchk$host") ;
	} else {
		&error("���M�ł��܂���B��x�f���ɖ߂��Ă��瑗�M�������Ă��������B","1");
	}

	# ���[�����M���O
	my $times = time;
	my $new = "$times<>$in{'name'}<>$in{'email'}<>$s_name<>$s_email<>$host<>$in{'no'}<>\n";
	if (-e "$mailchk$sendmaillog") {
		# ���[�����M���O���J��
		open(DAT,"+<$mailchk$sendmaillog");
		eval { flock(DAT, 1); };
		my $i = 1;
		my @new = ();
		while (<DAT>) {
			# �Â����O���폜
			if ($i < $spamlog_max) {
				push(@new,$_);
			}
			$i++;
		}
		close(DAT);

		# ���[�����M���O�X�V
		unshift (@new,$new);
		open(OUT,"+>$mailchk$sendmaillog");
		eval { flock(OUT, 2); };
		seek(OUT, 0, 0);
		print OUT @new;
		close(OUT);
	} else  {
		# �V�K���[�����M���O
		open(OUT,">$mailchk$sendmaillog");
		eval { flock(OUT, 2); };
		chmod (0606,"$mailchk$sendmaillog");
		print OUT $new;
	}

	# ���[���^�C�g��
	my $MailSub = "$in{'sub'}";
	#���[����M�҃A�h���X
	$s_email = "$s_name <$s_email>";
	#���[�����M�҃A�h���X
	my $Mailfrom = "$in{'name'} <$in{'email'}>";

	# ���[���{���̃^�O�E���s�𕜌�
	my $comment = $in{'comment'};
	$comment =~ s/&lt;/</g;
	$comment =~ s/&gt;/>/g;
	$comment =~ s/&amp;/&/g;
	$comment =~ s/<br>/\n/g;

	# ���[���{��
	my $MailBody = <<EOM;
�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
$title�̓��e�ɑ΂���
$in{'name'} ���񂩂� $s_name ����ւ̃��[���ł��B
�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
$comment
�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q
���̃��[���̓��e�ɂ��S�����肪�Ȃ����͉��L�܂ł��₢���킹�������B
http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}
�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P
EOM

	&jcode::convert(\$MailSub,'jis');
	&jcode::convert(\$MailBody,'jis');
	require $mimewpl;
	$s_email = &mimeencode($s_email);
	$Mailfrom = &mimeencode($Mailfrom);

	open(MAIL,"| $sendmail -t -i") || &error("���[�����M�Ɏ��s���܂���");
	print MAIL "Received: from YY-BOARD.$mode ($host [$addr]) by $ENV{'SERVER_NAME'} ($ver)\n";
	print MAIL "To: $s_email\n";
	print MAIL "From: $Mailfrom\n";
	print MAIL "Errors-To: $mailto\n";
	print MAIL "Subject: $MailSub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-IP: $addr\n";
	print MAIL "X-FROM-DOMAIN: $host\n";
	print MAIL "X-Mailer: $ver (http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'})\n\n";
	print MAIL "$MailBody\n";
	close(MAIL);

	&header;
	print <<EOM;
<div style="text-align: center;">
<hr width="350">
<h3>$s_name ����ֈ��Ƀ��[�������M����܂���</h3>
<form action="$bbscgi" method="$method">
<input type="submit" value="�f���֖߂�" class="post">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="list" value="$in{'list'}">
</form>
<hr width="350">
</div>
</body>
</html>
EOM
	exit;
}



1;
