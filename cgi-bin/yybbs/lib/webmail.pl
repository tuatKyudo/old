#┌──────────────────────────────────
#│ webmail.pl for YY-BOARD ver 2.00
#│ Copyright isso. April, 2008
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└──────────────────────────────────

#-------------------------------------------------
#  メール作成フォーム
#-------------------------------------------------
sub writemail {
	# リファラーチェック
	if (!$ENV{'HTTP_REFERER'}) {
		if ($referercheck != 2) {
			&error("メール送信フォームへは直接アクセスできません。");
		} else {
			# Internal Server Error
			&cgi_error;
		}
	}

	# 連続送信チェック
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
		# 連続送信
		if ($flg) {
			&error("連続送信はできません。");
		}
	}

	my ($s_name, $s_email, $s_smail, $s_msg, $s_sub, $s_no);
	# クッキーを取得
	my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	open(IN,"$logfile") || &error("ログファイル $logfile がありません。");
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

	if (!$webmail || $s_smail ne "1" || $s_email eq "") { &error("不正なアクセスです。"); }

	# コメントメッセージ
	my $res_msg = "\n\> $s_msg";
	$res_msg =~ s/&amp;/&/g;
	$res_msg =~ s/<br>/\r> /g;

	# コメントタイトル
	my $res_sub = $s_sub;
	$res_sub =~ s/<([^>]|\n)*>//g;

	# sendmailチェック
	if (-d $mailchk) {
		open(OUT,">$mailchk$host") || &error("送信できません。管理者にお問い合わせ下さい。");
		eval { flock(OUT, 2); };
		print OUT $host;
		close(OUT);
	} else {
		mkdir ($mailchk, 0707) || &error("送信できません。管理者にお問い合わせ下さい。");
		open(OUT,">$mailchk$host");
		eval { flock(OUT, 2); };
		print OUT $host;
		close(OUT);
	}

	# HTMLを出力
	&header;

	# ダミー
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
<input type="button" value="&lt;&lt; 戻る" onclick="history.back()">
<input type="hidden" name="list" value="$in{'list'}">
</form>
</div>
<div style="text-align: center;">
<hr width="500">
<h3>下記の内容で投稿者 $s_name さんにメールを送信します。</h3>
なお、いたずらメール防止のため、メール本文以外の送信情報を記録しております。
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
    <b style="color:#ff0000;">入力禁止</b>
  </td>
</tr>
<tr class="topdisp">
  <td nowrap>Title</td>
  <td>
    <input type="text" name="title" size="36" value="">
    <b style="color:#ff0000;">入力禁止</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>タイトル</b></td>
  <td>
    <input type="text" name="sub" size="36" value="$res_sub">
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>おなまえ</b></td>
  <td><input type="text" name="$name_key" size="36" value="$cnam"><b style="color:#ff0000;">※必須</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>Ｅメール</b></td>
  <td>
    <input type="hidden" name="mail" size="28" value="$enaddress">
    <input type="text" name="$mail_key" size="36" value="$ceml"><b style="color:#ff0000;">※必須</b>
  </td>
</tr>
<tr class="topdisp">
  <td nowrap><b style="color:#ff0000;">入力禁止</b></td>
  <td>
    <input type="text" name="$url_key" size="10" value="">
  </td>
</tr>
EOM
	print qq|<tr>  <td nowrap |;
	if (!$boardmode) {
		print qq|colspan="2" |;
	}
	print qq|class="form"><b>メッセージ</b>|;
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
    fcheck("value='送信する'><input t","<input t","ype='submit' name='submit' ","ype='reset' value='リセット'>");
    // -->
    </script>
    <noscript><br><b>Javascriptが無効なため送信できません。</b><br><br></noscript>
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
#  メール送信ルーチン
#-------------------------------------------------
sub sendmail {
	$spammail = 0;
	my ($s_smail,$s_email,$s_name);

	# POST限定
	if ($MethPost && !$post_flag) { &error("不正なアクセスです"); }

	open(IN,"$logfile") || &error("ログファイル $logfile がありません。");
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
		&error("送信できません。","1");
	}

	if ($in{'email'} eq "" || $in{'name'} eq "") {
		&error("Ｅメールとおなまえの入力は必須です。","1");
	}

	# Ｅメール入力
	if ($in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,3}/) {
		&error("Ｅメールの入力が不正です","1");
	}
	my $atmark = $in{'email'} =~ s/\@/\@/g;
	if ($atmark != 1) {
		&error("Ｅメールの入力が不正です","1");
	}

	# スパム送信対策
	my $acctime = &decode_bbsmode($in{"$bbscheckmode"});
	my $enadr = &encode_addr($addr);
	if($ipcheckmode) {
		if ($in{'mail'} ne $enadr) {
			&error("接続ホスト情報が不正なため送信できませんでした。","1");
		}
	} else {
		if ($in{'mail'} =~ /\@/) {
			&error("入力内容が不正なため送信できませんでした。","1");
		}
	}

	my $tcheck = abs(time - $acctime);
	if ($tcheck < $mintime || $tcheck > $maxtime) {
		&error("不正な送信は禁止されています。","1");
	}

	if ($in{'submit'} ne "送信する") {
		&error("正常にメールを送信できませんでした。","1");
	}

	if ($in{'url'} || $in{'subject'} || $in{'title'} || $in{'name'} =~ /https?\:\/\//i) {
		&error("入力内容が不正なため送信できませんでした。","1");
	}

	if (length($in{'comment'}) < length($in{'name'})) {
		&error("メッセージが短すぎるため送信できませんでした。","1");
	}

	if ($japanese) {
		if ($in{'comment'} !~ /(\x82[\x9F-\xF2])/) {
			&error("日本語での入力が必須です。(Japanese Only)","1");
		}
	}

	if (-e "$mailchk$host") {
		unlink("$mailchk$host") ;
	} else {
		&error("送信できません。一度掲示板に戻ってから送信し直してください。","1");
	}

	# メール送信ログ
	my $times = time;
	my $new = "$times<>$in{'name'}<>$in{'email'}<>$s_name<>$s_email<>$host<>$in{'no'}<>\n";
	if (-e "$mailchk$sendmaillog") {
		# メール送信ログを開く
		open(DAT,"+<$mailchk$sendmaillog");
		eval { flock(DAT, 1); };
		my $i = 1;
		my @new = ();
		while (<DAT>) {
			# 古いログを削除
			if ($i < $spamlog_max) {
				push(@new,$_);
			}
			$i++;
		}
		close(DAT);

		# メール送信ログ更新
		unshift (@new,$new);
		open(OUT,"+>$mailchk$sendmaillog");
		eval { flock(OUT, 2); };
		seek(OUT, 0, 0);
		print OUT @new;
		close(OUT);
	} else  {
		# 新規メール送信ログ
		open(OUT,">$mailchk$sendmaillog");
		eval { flock(OUT, 2); };
		chmod (0606,"$mailchk$sendmaillog");
		print OUT $new;
	}

	# メールタイトル
	my $MailSub = "$in{'sub'}";
	#メール受信者アドレス
	$s_email = "$s_name <$s_email>";
	#メール送信者アドレス
	my $Mailfrom = "$in{'name'} <$in{'email'}>";

	# メール本文のタグ・改行を復元
	my $comment = $in{'comment'};
	$comment =~ s/&lt;/</g;
	$comment =~ s/&gt;/>/g;
	$comment =~ s/&amp;/&/g;
	$comment =~ s/<br>/\n/g;

	# メール本文
	my $MailBody = <<EOM;
＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
$titleの投稿に対する
$in{'name'} さんから $s_name さんへのメールです。
￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
$comment
＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
このメールの内容にお心当たりがない方は下記までお問い合わせ下さい。
http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}
￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
EOM

	&jcode::convert(\$MailSub,'jis');
	&jcode::convert(\$MailBody,'jis');
	require $mimewpl;
	$s_email = &mimeencode($s_email);
	$Mailfrom = &mimeencode($Mailfrom);

	open(MAIL,"| $sendmail -t -i") || &error("メール送信に失敗しました");
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
<h3>$s_name さんへ宛にメールが送信されました</h3>
<form action="$bbscgi" method="$method">
<input type="submit" value="掲示板へ戻る" class="post">
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
