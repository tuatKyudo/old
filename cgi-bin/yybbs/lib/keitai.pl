#┌─────────────────────────────────
#│ keitai.pl for YY-BOARD ver 2.00
#│ Copyright isso. April, 2008
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

#------------------#
#  新着順一覧表示  #
#------------------#
sub k_new {
	my (%no,%reno,%sub);

	if ($mode eq "k_admin") {
		if ($in{'pass'} eq "") { &enter; }
		if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }
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
		print qq|<input type="submit" value="掲示板へ戻る">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klist">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="親記事">\n</form>\n<br>\n|;
		print qq|<form action="$admincgi" method="$method">\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=klist">親記事順</a>/\n|;
		print qq|<a href="$bbscgi?mode=newpost">投稿</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">管理</a>\n<hr>\n|;
	}

	# ソート処理
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
			print qq|<input type="checkbox" name="no" value="$no{$_}">削除 |;
			print qq|[$no{$_}] <a href="$bbscgi?mode=kaview&no=$no{$_}&kmode=admin">$sub{$_}</a><br>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=kmsgview&no=$no{$_}">$sub{$_}</a><br>\n|;
		}
	}

	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<br>\n<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|パスワード: <input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="job" value="dele">\n|;
		print qq|<input type="submit" value="削除">\n</form>\n|;
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
		print qq|<input type="submit" value="前画面">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="submit" value="次画面">\n</form>\n|;
	}

	print qq|$copyright\n|;
	print qq|</body>\n</html>\n|;
	exit;
}

#--------------------#
#  タイトル一覧表示  #
#--------------------#
sub k_list {
	my (%no,%reno,%sub,%num,%cnt);

	if ($mode eq "k_admin") {
		if ($in{'pass'} eq "") { &enter; }
		if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }
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
		print qq|<input type="submit" value="掲示板へ戻る">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="knew">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="新着順">\n</form>\n<br>\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=knew">新着順</a>/\n|;
		print qq|<a href="$bbscgi?mode=newpost">投稿</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">管理</a>\n<hr>\n|;
	}

	# ソート処理
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
			print qq|<a href="$bbscgi?mode=klview&no=$no{$_}">$sub{$_}</a> ($cnt{$no{$_}}件)\n<br>\n|;
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
		print qq|<input type="submit" value="前画面">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="$mode">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="submit" value="次画面">\n</form>\n|;
	}

	print qq|$copyright|;
	print qq|</body></html>\n|;
	exit;
}

#----------------------#
#  スレッド内順表示  #
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
		print qq|<input type="submit" value="掲示板へ戻る">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klist">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="親記事順">\n</form>\n|;
		print qq|<form action="$bbscgi" method="$method">\n\n|;
		print qq|<input type="hidden" name="mode" value="knew">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="新着順">\n</form>\n<br>\n|;
		print qq|<form action="$admincgi" method="$method">\n|;
	} else {
		print qq|<a href="$khome">TOP</a>/\n|;
		print qq|<a href="$bbscgi?mode=klist">親記事順</a>/\n|;
		print qq|<a href="$bbscgi?mode=knew">新着順</a>/\n|;
		print qq|<a href="$bbscgi?mode=k_admin">管理</a>\n<hr>\n|;
	}

	# ソート処理
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
			print qq|<input type="checkbox" name="no" value="$no{$_}">削除 |;
			print qq|[$no{$_}] <a href="$bbscgi?mode=kaview&kmode=admin&no=$no{$_}">$sub{$_}</a>\n<br>\n|;
		} else {
			print qq|<a href="$bbscgi?mode=kmsgview&no=$no{$_}">$sub{$_}</a>\n<br>\n|;
		}
	}

	if ($mode eq "k_admin" || $in{'kmode'} eq "admin") {
		print qq|<br>\n<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="job" value="dele">\n|;
		print qq|パスワード: <input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="削除">\n</form>\n|;
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
		print qq|<input type="submit" value="前画面">\n</form>\n|;
	}
	if ($next < $i) {
		print qq|<form action="$bbscgi" method="$method">\n|;
		print qq|<input type="hidden" name="mode" value="klview">\n|;
		print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="hidden" name="page" value="$next">\n|;
		print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
		print qq|<input type="submit" value="次画面">\n</form>\n|;
	}

	print qq|$copyright\n|;
	print qq|</body>\n</html>\n|;
	exit;
}

#------------------#
#  メッセージ表示  #
#------------------#
sub k_msg {
	&header;
	print qq|$title\n<hr>\n|;
	if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
		print qq|$keitai_mode\n<br>\n|;
	}
		if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
			print qq|<a href="$bbscgi?mode=klist&kmode=admin">親記事順</a>/\n|;
			print qq|<a href="$bbscgi?mode=knew&kmode=admin">新着順</a>\n<hr>\n|;
		} else {
			print qq|<a href="$khome">TOP</a>/\n|;
			print qq|<a href="$bbscgi?mode=klist">親記事順</a>/\n|;
			print qq|<a href="$bbscgi?mode=knew">新着順</a>/\n|;
			print qq|<a href="$bbscgi?mode=k_admin">管理</a>\n<hr>\n|;
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
			# タイトル
			$res_sub = $sub;
			$res_sub =~ s/<([^>]|\n)*>//g;
			if ($res_sub =~ /^Re(.*)/) { $res_sub = "Re$1"; }
			else { $res_sub = "Re: $res_sub"; }
			# URL自動リンク
			if ($k_link) { $msg = &auto_link($msg); }
			# 引用部色変更
			if ($refcol) {
				$msg =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
			}
			# コメント色変更
			$msg = "<font color=\"$color\">$msg</font>";
			print qq|No\.$no<br>\n$dat<br>\n題名: $sub<br>\n投稿者: $name\n<hr>\n|;
			print qq|<font color="$color">$msg</font>\n|;
			if ($mode eq "kaview" || $in{'kmode'} eq "admin") {
				print qq|<form action="$admincgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="admin">\n|;
				print qq|<input type="hidden" name="kmode" value="$in{'kmode'}">\n|;
				print qq|<input type="hidden" name="job" value="dele">\n|;
				print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
				print qq|<input type="password" name="pass" size="8" value="$in{'pass'}">\n|;
				print qq|<input type="submit" value="削除">\n</form>\n|;
			} else {
				print qq|<form action="$bbscgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="newpost">\n|;
				print qq|<input type="hidden" name="kaction" value="comment">\n|;
				print qq|<input type="hidden" name="res_sub" value="$res_sub">\n|;
				print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
				print qq|<input type="hidden" name="oya" value="$oya">\n|;
				print qq|<input type="submit" value="返信">\n</form>\n|;
				print qq|<form action="$bbscgi" method="$method">\n|;
				print qq|<input type="hidden" name="mode" value="klview">\n|;
				print qq|<input type="hidden" name="no" value="$oya">\n|;
				print qq|<input type="hidden" name="page" value="$in{'page'}">\n|;
				print qq|<input type="submit" value="リストにもどる">\n</form>\n|;
			}
		}
	}
	close(IN);

	if ($mode eq "kmsgview") { &edit_form; }
	print qq|</body>\n</html>\n|;
	exit;
}

#----------------#
#  投稿フォーム  #
#----------------#
sub k_form{
	# クッキーを取得
	my ($cname,$cmail,$curl,$cpwd,$cico,$ccol) = &get_cookie;

	my $access = &encode_bbsmode();
	my $enaddress = &encode_addr();
	if ($keychange && $_[0] ne "edit") {
		$url_key  = 'email'; $mail_key = 'url'; $name_key = 'comment'; $comment_key = 'name';
	} else { $url_key  = 'url'; $mail_key = 'email'; $name_key = 'name'; $comment_key = 'comment'; }

	# 投稿キー
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	&header;
	print qq|[<a href="$bbscgi">掲示板へ戻る</a>]\n|;
	# 修正時
	if ($_[0] eq "edit") {
		($edittype,$no,$reno,$date,$cname,$cmail,$res_sub,$res_msg,$curl,$host,$pw,$col,$ico,$tm,$sm) = @_;

		print qq|修正フォーム<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<!-- //\n<input type="hidden" name="mode" value="write">\n// -->\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<input type="hidden" name="mode" value="edit">\n|;
		print qq|<input type="hidden" name="kaction" value="edit">\n|;
		print qq|<input type="hidden" name="pwd" value="$pw">\n|;
		print qq|<input type="hidden" name="no" value="$no">\n|;
		print qq|<input type="hidden" name="reno" value="$reno">\n|;
	# 返信時
	} elsif ($in{'kaction'} eq 'comment') {
		$res_sub = $in{'res_sub'};
		print qq|<hr>- 返信フォーム -<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<!--    //\n<input type="hidden" name="mode" value="write">\n//     -->\n|;
		print qq|<input type="hidden" name="page" value="$page">\n|;
		print qq|<input type="hidden" name="kaction" value="res_msg">\n|;
		print qq|<input type="hidden" name="no" value="$in{'no'}">\n|;
		print qq|<input type="hidden" name="reno" value="$in{'oya'}">\n|;
	# 新規時
	} else {
		print qq|<hr>- 新規投稿フォーム -<hr>\n|;
		print qq|<form action="$registcgi" method="$method">\n|;
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
		print qq|<!--    //\n<input type="hidden" name="mode" value="write">\n//     -->\n|;
	}

	if ($allowmode) {
		if ($_[0] ne "edit" && $in{'kaction'} ne "comment") {
			print qq|<b> 投稿内容は管理者が許可するまで表\示されません。 </b>\n<br>\n|;
		}
	}

	print qq|おなまえ <input type="text" name="$name_key" size="20" value="$cname"><br>\n|;

	if ($aikotoba) {
		print qq|<b>合い言葉</b><br>\n|;
		print qq|<input type="text" name="aikotoba" size="10" value="$caikotoba">|;
		print qq|<font color="#ff0000">※必須</font><br>\n|;
		print qq|$hint<br>\n|;
	}

	print qq|Ｅメール <input type="hidden" name="mail" size="28" value="$enaddress">\n|;
	print qq|<input type="text" name="$mail_key" size="20" value="$cmail">\n|;
	if ($in_email) {
		print qq|<font color="#ff0000">必須</font>\n|;
	}
	print qq|<br>\n|;

	print qq|タイトル <input type="text" name="sub" size="20" value="$res_sub">\n|;
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

	print qq|メッセージ<br>\n|;
	print qq|<textarea name="$comment_key" rows="5" cols="20" wrap="soft">$res_msg</textarea><br>\n|;

	# 管理者アイコンを配列に付加
	@ico1 = split(/\s+/, $ico1);
	@ico2 = split(/\s+/, $ico2);
	if ($my_icon) {
		push(@ico1,$my_gif);
		push(@ico2,"管理者用");
	}
	if ($iconMode) {
		print qq|アイコン <select name="icon">\n|;
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

	# 色情報
	print qq|色 \n|;
	my @col = split(/\s+/, $color);
	if ($col eq "") { $col = 0; }
	my $acol = $#col;
	# 管理者色
	if ($adminchk && $nam eq $admin_id) {
		$acol = $#col+1; $col[$acol] = $a_color;
	}
	foreach (0 .. $acol) {
		if ($col eq $col[$_] || $col eq $_) {
			print qq|<input type="radio" name="color" value="$_" checked>|;
			print qq|<font color="$col[$_]">■</font>\n|;
		} else {
			print qq|<input type="radio" name="color" value="$_">|;
			print qq|<font color="$col[$_]">■</font>\n|;
		}
	}
	print qq|<br>\n|;

	if ($_[0] eq "edit") {
		print qq|<input type="submit" value=" 記事を修正する "></form><br>\n|;
	} else {
		print qq|削除キー <input type="password" name="pwd" size="8" value="$cpwd" maxlength=\8\>\n|;
		if ($in_pwd) {
			print qq|<b><font color="#ff0000">※必須</font></b>|;
		}
		print qq|<br>(英数字で8文字以内)<br>\n|;
		if ($regist_key) {
			print qq|<input type="text" name="regikey" size="6" style="ime-mode:inactive" value="">\n<br>\n|;
			print qq|（投稿時 <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="投稿キー">|;
			print qq| を入力してください）<br>\n|;
			print qq|<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
		}
		print qq|<input type="hidden" name="mode" value="$writevalue">\n|;
		print qq|<input type="submit" name="submit" value=" 記事を投稿する "></form>\n|;
	}
	print qq|</body>\n</html>\n|;
	exit;
}

#------------#
#  入室画面  #
#------------#
sub enter {
	&header;
	print <<EOM;
<a href="$bbscgi">掲示板へ戻る</a>
<hr>
管理者パスワード: 
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="k_admin">
<input type="hidden" name="kmode" value="admin">
<input type="password" name="pass" size="8">
<input type="submit" value=" 認証 "></form>
</body>
</html>
EOM
	exit;
}

#------------#
#  記事削除  #
#------------#
sub k_dele {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# 削除情報をマッチング
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

	# ログを更新
	unshift(@new,$top);
	seek(DAT, 0, 0);
	print DAT @new;
	truncate(DAT, tell(DAT));
	close(DAT);

	&header;
	print <<EOM;
<form action="$bbscgi" method="$method">
<input type="submit" value="掲示板へ戻る">
</form>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="knew">
<input type="hidden" name="kmode" value="$in{'kmode'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="管理モード">
</form>
</body>
</html>
EOM
	exit;
}

#----------------#
#  修正フォーム  #
#----------------#
sub edit_form {
	print <<EOM;
<hr>
- 記事の修正・削除 - <br>
<form action="$registcgi" method="$method">
処理選択 <select name="mode">
<option value="edit">修正
<option value="dele">削除</select><br>
記事No. <input type="text" name="no" size="6" value="$in{'no'}"><br>
削除キー <input type="password" name="pwd" size="8" value=""></small>
<input type="submit" value="実行"></form>
<hr>
$copyright
EOM
	exit;
}

#----------------#
#  書き込み完了  #
#----------------#
sub k_after {
	&header;
	print qq|<a href="$bbscgi">掲示板へ戻る</a>\n|;
	print qq|</body></html>\n|;
	exit;
}

1;
