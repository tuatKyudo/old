#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ read.cgi - 2007/09/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#│
#│ YY-BOARD Antispam Version Modified by isso.
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

# 外部ファイル取込
require './init.cgi';
require $jcode;

#-------------------------------------------------
# 設定チェック
#-------------------------------------------------
# ログファイル
unless(-e "$logfile") {
	&error("ログファイル $logfile がありません。");
}

# 過去ログデータファイル
if($pastkey) {
	unless(-e "$nofile") {
		&error("過去ログデータファイル $nofile  がありません。");
	}
}

# カラーデータファイル
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
	&error("カラーデータファイル $colordata がありません。");
}

# 表示モード設定
if ($boardmode && -s "$colordata") { &read_color; }

#-------------------------------------------------
# メイン処理
#-------------------------------------------------
&agent;
&decode;
&axsCheck;

# 自動閉鎖
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
#  記事個別閲覧
#-------------------------------------------------
sub read_log {
	# 記事を展開
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

	if (!$data) { &error("不明なアクセスです"); }

	# ヘッダを出力
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# タイトル部
	print qq|<div align="center">\n|;
	if ($banner1 ne "<!-- 上部 -->") { print "$banner1<p>\n"; }
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
		print qq|<input type="submit" value="リストに戻る" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$homepage" method="get">\n<td nowrap>\n|;
		print qq|<input type="submit" value="ホームに戻る" class="menu">\n</td>\n</form>\n|;

		# 新規投稿
		if (!$in{'list'}) { $in{'list'} = 'thread'; }
		if ($in{'list'} ne "thread") {
			print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
			print qq|<input type="hidden" name="mode" value="postform">\n|;
			print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
			print qq|<input type="submit" value="新規投稿" class="menu">\n</td>\n</form>\n|;
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
		print qq|<input type="submit" value="留意事項" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="find">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="submit" value="ワード検索" class="menu">\n</td>\n</form>\n|;

		print qq|<form action="$bbscgi" method="post">\n<td nowrap>\n|;
		print qq|<input type="hidden" name="mode" value="past">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|<input type="submit" value="過去ログ" class="menu">\n</td>\n</form>\n| if ($pastkey);

		print qq|<form action="$admincgi" method="post"><td nowrap>\n\n|;
		print qq|<input type="hidden" name="mode" value="admin">\n|;
		print qq|<input type="submit" value="管理用" class="menu">\n</td>\n</form>\n|;

		print qq|</tr></table>\n|;
		print qq|</div>\n<br>\n|;

	} else {

		print <<EOM;
<hr width="90%">
[<a href="$bbscgi?list=$in{'list'}&page=$in{'page'}">リストに戻る</a>]
[<a href="$homepage" target="_top">ホームに戻る</a>]
EOM

		if (!$in{'list'}) { $in{'list'} = 'thread'; }
		if ($in{'list'} ne "thread") {
			print qq|[<a href="$bbscgi?mode=form&list=$in{'list'}">新規投稿</a>]\n|;
		}

		foreach ( 'thread', 'tree', 'topic', 'new', ) {
			next if ($in{'list'} eq $_);

			print qq|[<a href="$bbscgi?list=$_">$list_type{$_}</a>]\n|;
		}

		print <<EOM;
[<a href="$bbscgi?mode=howto&list=$in{'list'}">留意事項</a>]
[<a href="$bbscgi?mode=find&list=$in{'list'}">ワード検索</a>]
EOM

		# 過去ログのリンク部を表示
		if ($pastkey) {
			print qq|[<a href="$bbscgi?mode=past&list=$in{'list'}">過去ログ</a>]\n|;
		}

	print <<EOM;
[<a href="$admincgi">管理用</a>]
<hr width="90%"></div>
EOM
	}

	# 記事一括のとき
	if ($mode eq "all") { &all_list; }

	# 閲覧記事
	my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/, $data);

	# 整形
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
  <td>記事No</td><td>： <b>$no</b></td>
</tr>
<tr>
  <td>タイトル</td><td>： <b style="color:$subcol">$sub</b></td>
</tr>
<tr>
  <td>投稿日</td><td>： $dat</td>
</tr>
<tr>
  <td>投稿者</td><td>： <b>$nam</b></td>
</tr>
EOM
	if ($url) {
		print qq|<tr>\n  <td>URL</td><td>： $url</td>\n</tr>\n|;
	}
	print qq|</table>\n<p>\n|;

	# 引用部色変更
	if ($refcol) {
		$com =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
	}

	# URL自動リンク
	if ($autolink) { $com = &auto_link($com); }

	# 記事
	if ($iconMode) {
		print qq|<table><tr><td><img src="$imgurl/$ico"></td>\n|;
		print qq|<td width="8"></td>\n|;
		print qq|<td style="color:$col">$com</td></tr></table>\n|;
	} else {
		print qq|<div style="margin-left:22px; margin-top:6px">\n|;
		print qq|<span style="color:$col">$com</span>\n|;
	}

	local ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	# 投稿者編集フォーム
	if ($boardmode) {
		print qq|<form action="$registcgi" method="$method">\n|;
		if ($pw) {
			if ($cnam) {
				if ($cnam =~ /\Q$author\E/i || $author =~ /\Q$cnam\E/i) {
					print qq|<div align="right">\n|;
					print qq|投稿者 <select name="mode">\n|;
					print qq|<option value="edit">修正\n|;
					print qq|<option value="dele">削除</select>\n|;
					print qq|<input type="hidden" name="no" value="$no">\n&nbsp;|;
					print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
					print qq|削除キー <input type="password" name="pwd" size="8" maxlength="8" value="$cpwd">\n|;
					print qq|<input type="submit" value="送信" class="post"></div>\n|;
				}
			}
		}
		print qq|</td>\n</tr>\n</table>\n</div>\n|;
		print qq|</form>\n|;
	} else {
		print qq|<hr>\n|;
	}

	print <<EOM;
<b>- 関連ツリー</b>
<p>
EOM

	# 関連ツリー
	my $i = 0;
	local($oya,$resub);
	foreach (@tree) {
		$i++;
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($reno && $i == @tree) {
			print "&nbsp" x 5;
			print "└ ";
		} elsif ($reno && $i > 1) {
			print "&nbsp" x 5;
			print "├ ";
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

		# 親
		if (!$reno) {
			print qq|<a href="$readcgi?mode=all&list=tree&no=$no" title="ツリーを一括表\示">▼</a> |;
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
#  記事一括閲覧
#-------------------------------------------------
sub all_list {
	print <<EOM;
<blockquote>
EOM

	# 関連ツリー
	my $i = 0;
	local($oya,$resub,$list);
	foreach (@tree) {
		$i++;
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($reno && $i == @tree) { print "&nbsp;└ "; }
		elsif ($reno && $i > 1) { print "&nbsp;├ "; }

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

		# ツリー表示
		print qq|<a href="$readcgi?mode=all&list=$in{'list'}&no=$oya#$no">$sub</a> - <b>$nam</b> $dat <span style="color:$subcol">No.$no</span>\n|;
		if (time - $tm < $new_time * 3600) {
			print qq|&nbsp;$newmark\n|;
		}
		print qq|<br>\n|;

		# 親記事
		if (!$reno) {
			push(@view,$no);
		# レス記事
		} else {
			$res{$reno} .= "$no,";
		}

		# 題名の長さ
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

	# クッキー取得
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	require $list_log_thread;
	&list_log_thread;

	&reply_form;
}

#-------------------------------------------------
#  返信専用フォーム
#-------------------------------------------------
sub reply_form {

	if ($boardmode) {
			print qq|<p>\n<br>\n|;
	} else {
			print qq|<p>\n<hr>\n|;
	}

	print <<EOM;
<b>- 返信フォーム</b>
<p>
EOM

	# タイトル名
	if ($resub !~ /^Re\:/) { $resub = "Re: $resub"; }

	# 投稿キー
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

	# 投稿フォーム
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
		print qq|<b> 投稿内容は管理者が許可するまで表\示されません。 </b>|;
		print qq|</td>\n</tr>\n</table>\n<br>\n|;
	}

	# フォーム
	if (!$re_box) { $cref = 0; }
	require $formpl;
	&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$resub,'',$csmail,$caikotoba,$cref,'reply');
	print qq|</form>\n|;

	# ユーザメンテフォーム（トピック表示の場合）
	if ($in{'list'} eq "topic") {
		if ($boardmode) {
			print qq|<br>\n<br>\n|;
			print qq|<b>- 記事修正＆削除フォーム</b><br>\n<br>\n|;
			print qq|<table border="0" cellspacing="10" cellpadding="0" class="thread">\n<tr><td>\n|;
		} else {
			print qq|<hr>\n|;
			print qq|<b>- 記事修正＆削除フォーム</b><br>\n<br>\n|;
		}
		print qq|<form action="$registcgi" method="post">\n|;
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
		print qq|投稿者 <select name="mode" class="f">\n|;
		print qq|<option value="edit">修正\n|;
		print qq|<option value="dele">削除</select>\n|;
		print qq|No.<input type="text" name="no" size="3" class="f" style="ime-mode:inactive">\n|;
		print qq|削除キー<input type="password" name="pwd" size="4" maxlength="8" value="$cpwd" class="f">\n|;
		print qq|<input type="submit" value="送信">|;
		if ($boardmode) { print qq|</td>\n</tr>\n</table>\n</form>\n|; }
	}

	print <<EOM;
</blockquote>
</body>
</html>
EOM
	exit;
}


