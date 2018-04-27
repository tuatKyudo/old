#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ admin.cgi - 2007/09/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#│ 
#│ 
#│ ――――――――――――――[注意事項]――――――――――――――
#│ 
#│ 本スクリプトについて、KENT WEBサポート掲示板への質問は禁止です。
#│ 利用規定を守らない場合には本改造スクリプトの使用を一切認めません。
#│ 
#│ ――――――――――――――[注意事項]――――――――――――――
#│ 
#│ 
#│ YY-BOARD Antispam Version Modified by isso.
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

# 外部ファイル取込
require './init.cgi';
require $jcode;

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
#  管理モード
#-------------------------------------------------
sub admin {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# ページ繰り越し
	foreach ( keys(%in) ) {
		if (/^page:(\d+)$/) {
			$page = $1;
			last;
		}
	}

	# 修正画面
	if ($in{'job'} eq "edit" && $in{'no'}) {

		if ($in{'no'} =~ /\0/) { &error("修正記事の選択は１つのみです"); }

		local($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm);

		open(IN,"$logfile") || &error("Open Error: $logfile");
		my $top = <IN>;
		while (<IN>) {
			chomp;
			($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);

			if ($no == $in{'no'}) { last; }
		}
		close(IN);

		# 管理者
		my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
		if ($adminchk) {
			if ($cnam eq $admin_id && $cpwd eq $pass) {
				$nam = $admin_id;
				if($a_color) { $col = $a_color; }
			}
		}

		# 修正フォーム
		&edit_form($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm);

	# 修正実行
	} elsif ($in{'job'} eq "edit2" && $in{'no'}) {

		if ($in{'url'} eq "http://") { $in{'url'} = ''; }

		my @col = split(/\s+/, $color);
		my @ico1 = split(/\s+/, $ico1);
		if ($my_icon) { push(@ico1,$my_gif); }
		$in{'icon'} = $ico1[$in{'icon'}];

		# 管理者
		if ($adminchk && $in{'name'} eq $admin_id) {
			@color = split(/\s+/, $color); $acol = $#color+1;
			$in{'color'} = $acol; $col[$acol] = $a_color;
			$in{'name'} = $a_name;
		}

		# URL自動リンク
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

		# 更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# 削除
	} elsif ($in{'job'} eq "dele" && $in{'no'}) {

		my @del = split(/\0/, $in{'no'});

		# 削除情報をマッチング
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

		# 更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		if ($keitai ne 'p') {
			&header;
			print <<EOM;
<a href="$bbscgi">掲示板へ戻る</a>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="k_admin">
<input type="hidden" name="kmode" value="admin">
<input type="password" name="pass" size="8" value="$in{'pass'}">
<input type="submit" value=" 管理モード " class="menu"></form>
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
<input type="submit" value="掲示板に戻る" class="menu">
</form>
</td>
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="change_mode">
<input type="hidden" name="pass" value="$in{'pass'}">
EOM
	if ($boardmode) {
		print qq|<input type="hidden" name="boardmode" value="1">\n|;
		print qq|<input type="submit" value=" YY-BOARD形式に戻す " class="menu">\n|;
	} else {
		print qq|<input type="hidden" name="boardmode" value="0">\n|;
		print qq|<input type="submit" value=" 新表\示形式に変更 " class="menu">\n|;
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
<input type="submit" value=" カラーモード設定 " class="menu">
</form>
</td>
EOM
	}


	# 掲示板再開
	if ($clday) {
		my $last = (stat $logfile)[9];
		if (time - $last > $clday*24*3600) {
			print <<EOM;
<td>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="reopen">
<input type="submit" value="掲示板再開" class="menu">
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
<input type="submit" value="エラーログ ($i件)" class="menu">
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
<input type="submit" value="NGワードの一括編集" class="menu">
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
<input type="submit" value="$postmode ($i件)" class="menu">
</form>
</td>
EOM
	}

	if($webmail && (-e "$mailchk$sendmaillog")) {
	print <<EOM;
<td><form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="sendmaillog">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="送信履歴を閲覧" class="menu">
</form>
</td>
EOM
	}

	print <<EOM;
</tr>
</table>
<hr>
<ul>
<li>処理を選択し、記事をチェックして送信ボタンを押して下さい。</li>
<li>親記事を削除するとレス記事も一括して削除されます。</li>
</ul>
<form action="$admincgi" method="post">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="pass" value="$in{'pass'}">
処理：
<select name="job">
<option value="edit">修正
<option value="dele">削除
</select>
<input type="submit" value="送信する" class="post"><br>
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

		# 削除チェックボックス
		print qq|<dl>\n|;
		if ($res) { print qq|<dd>\n|; } else { print qq|&nbsp;|; }
		print qq|<input type="checkbox" name="no" value="$no">|;
		print qq|[<b>$no</b>] <b style="color:$subcol">$sub</b>\n|;
		print qq|投稿者：<b>$nam</b> 投稿日：$dat &lt;<span style="color:$subcol">$hos</span>&gt;\n|;
		if ($res) { print qq|</dd>\n|; }
		print qq|<dd style="font-size:11px; color:$col;">$com</dd>\n|;
		print qq|</dl>\n|;
	}
	close(IN);
	if ($boardmode) { print qq|<br>\n</td>\n</tr>\n</table>\n</div>\n<br>\n|; }
	else { print qq|<dt><hr>\n</dl>|; }

	# 繰り越しページ
	my $next = $page + $pastView;
	my $back = $page - $pastView;

	if ($back >= 0) {
		print qq|<input type="submit" name="page:$back" value="前の$pastView組" class="post">\n|;
	}
	if ($next < $i) {
		print qq|<input type="submit" name="page:$next" value="次の$pastView組" class="post">\n|;
	}

	print <<EOM;
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub enter {
	&header;
	print <<EOM;
<blockquote>
<table border="0" cellspacing="0" cellpadding="26" width="400">
<tr><td align="center">
	<fieldset>
	<legend>
	▼管理パスワード入力
	</legend>
	<form action="$admincgi" method="post">
	<input type="password" name="pass" size="16">
	<input type="submit" value=" 認証 " class="post">
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
#  修正画面
#-------------------------------------------------
sub edit_form {
	local($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = @_;

	$com =~ s/<br>/\n/g;

	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }
	print <<EOM;
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; 前画面に戻る" class="post">
</form>
▽変更する部分のみ修正して送信ボタンを押して下さい。
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
#  カラーモード設定
#-------------------------------------------------
sub set_cmode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	&header;
	print <<EOM;
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; 掲示板へ" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu /">
</form>
</td></tr>
</table></div>
<hr>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="cmode">
<input type="hidden" name="pass" value="$in{'pass'}">
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">カラーモードを変更することができます。</td>
</tr>
<tr>
<td bgcolor="$tbl_col0">
<table border="$border" cellspacing="1" cellpadding="5">
<td bgcolor="$tblcol">
EOM

	open(COL,"$colorfile") || &error("カラーモードデータファイル $colorfile がありません。");
	$colormode = <COL>;
	close(COL);

	print "カラーモードを&nbsp;<select name=colormode>\n";
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
	"<option value=1 $selected1>ブルー系",
	"<option value=2 $selected2>ピンク系",
	"<option value=3 $selected3>オレンジ系",
	"<option value=4 $selected4>グリーン系",
	"<option value=5 $selected5>イエロー系",
	"<option value=6 $selected6>ヴァイオレット系",
	"<option value=7 $selected7>ホワイト系",
	"<option value=8 $selected8>グレー系",
	"<option value=9 $selected9>ブラック系",
	"</select>&nbsp;に&nbsp;\n";

	print <<EOM;
<input type="submit" value="設定する" class="post">
</td></tr></table>
</td></tr></table>
</form>
<br>
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">
カラーモードを変更後に、下記の設定を設定を変更することで掲示板を詳細にカスタマイズすることができます。
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
<td>背景色</td><td><input type="text" name="bgcolor" size="8" value="$bgcolor"></td>
<td>文字色</td><td><input type="text" name="text" size="8" value="$text"></td>
<td>カウンタ色</td><td><input type="text" name="cntCol" size="8" value="$cntcol"></td>
<td>タイトル文字色</td><td><input type="text" name="tCol" size="8" value="$tCol"></td>
</tr><tr>
<td>記事表\示部の下地色</td><td><input type="text" name="tblCol" size="8" value="$tblcol"></td>
<td>親記事欄背景色</td><td><input type="text" name="tbl_col0" size="8" value="$tbl_col0"></td>
<td>スレッド枠サイズ</td><td><input type="text" name="thr_brd" size="8" value="$thr_brd"></td>
<td>スレッド全体幅</td><td><input type="text" name="width" size="8" value="$width"></td>
</tr><tr>
<td>投稿フォーム背景色</td><td><input type="text" name="frm_bc" size="8" value="$frm_bc"></td>
<td>投稿フォーム文字色</td><td><input type="text" name="frm_tx" size="8" value="$frm_tx"></td>
<td>投稿フォーム枠色</td><td><input type="text" name="frm_brd" size="8" value="$frm_brd"></td>
<td>投稿フォーム枠サイズ</td><td><input type="text" name="frm_solid" size="8" value="$frm_solid"></td>
</tr><tr>
<td>ボタン文字色</td><td><input type="text" name="btx_col" size="8" value="$btx_col"></td>
<td>ボタン枠色</td><td><input type="text" name="btn_solid" size="8" value="$btn_solid"></td>
<td>メニュー文字色</td><td><input type="text" name="menu_chr" size="8" value="$menu_chr"></td>
<td>メニュー背景色</td><td><input type="text" name="menu_bg" size="8" value="$menu_bg"></td>
</tr><tr>
<td>メニュー枠色</td><td><input type="text" name="menu_solid" size="8" value="$menu_solid"></td>
<td>メニュー枠サイズ</td><td><input type="text" name="menu_brd" size="8" value="$menu_brd"></td>
<td>タイトル一覧背景色</td><td><input type="text" name="allt_col" size="8" value="$allt_col"></td>
<td>タイトル一覧枠色</td><td><input type="text" name="allt_solid" size="8" value="$allt_solid"></td>
</tr><tr>
<td>タイトル一覧枠サイズ</td><td><input type="text" name="allt_brd" size="8" value="$allt_brd"></td>
<td>コメント欄背景色</td><td><input type="text" name="tbl_col1" size="8" value="$tbl_col1"></td>
<td>テキストエリア枠サイズ</td><td><input type="text" name="tarea_brd" size="8" value="$tarea_brd"></td>
<td>入力欄枠サイズ</td><td><input type="text" name="btn_brd" size="8" value="$btn_brd"></td>
</tr><tr>
<td>投稿フォーム下地色</td><td><input type="text" name="formCol1" size="8" value="$formCol1"></td>
<td>投稿フォーム文字色</td><td><input type="text" name="formCol2" size="8" value="$formCol2"></td>
<td>投稿ボタン文字色</td><td><input type="text" name="post_chr" size="8" value="$post_chr"></td>
<td>投稿ボタン背景色</td><td><input type="text" name="post_bg" size="8" value="$post_bg"></td>
</tr><tr>
<td>投稿ボタン枠色</td><td><input type="text" name="post_solid" size="8" value="$post_solid"></td>
<td>投稿ボタン枠サイズ</td><td><input type="text" name="post_brd" size="8" value="$post_brd"></td>
<td>投稿キー画像の文字色</td><td><input type="text" name="moji_col" size="8" value="$moji_col"></td>
<td>投稿キー画像の背景色</td><td><input type="text" name="back_col" size="8" value="$back_col"></td>
</tr><tr>
<td>ラジオボタン枠サイズ</td><td><input type="text" name="radio_brd" size="8" value="$radio_brd"></td>
<td>スレッド全体枠幅</td><td><input type="text" name="border" size="8" value="$border"></td>
<td>スレッド枠幅</td><td><input type="text" name="cellspacing" size="8" value="$cellspacing"></td>
<td>スレッド枠余白</td><td><input type="text" name="cellpadding" size="8" value="$cellpadding"></td>
</tr><tr>
<td>親記事マーク</td><td><input type="text" name="topmark" size="8" value="$topmark"></td>
<td>コメントマーク</td><td><input type="text" name="comark" size="8" value="$comark"></td>
<td>コメント欄左マージン</td><td><input type="text" name="margin_left" size="8" value="$margin_left"></td>
<td>コメント欄右マージン</td><td><input type="text" name="margin_right" size="8" value="$margin_right"></td>
</tr><tr>
<td>記事 [タイトル] 色</td><td><input type="text" name="subCol" size="8" value="$subcol"></td>
<td>記事 [タイトル] 文字数</td><td><input type="text" name="sub_len" size="8" value="$sub_len"></td>
<td>引用部文字色</td><td><input type="text" name="refcol" size="8" value="$refcol"></td>
<td>ツリー選択記事背景色</td><td><input type="text" name="tree_bc" size="8" value="$tree_bc"></td>
</tr><tr>
<td>ボタン背景色</td><td><input type="text" name="btn_col" size="8" value="$btn_col"></td>
<td>メッセージ行間隔</td><td><input type="text" name="lheight" size="8" value="$lheight"></td>
EOM
	print "<td>背景画像を</td><td><select name=\"scroll\">\n";
	$selected0 = ""; $selected1 = "";
	if ($scroll eq "1") { $selected1 = "selected";
	} else { $selected0 = "selected"; }
	print "<option value=\"0\" $selected0>スクロールする",
	"<option value=\"1\" $selected1>固定する",
	"</select></td>\n";

	print "<td>メッセージ欄背景画像を</td><td><select name=\"thr_bg\">\n";
	$selected0 = ""; $selected1 = "";
	if ($thr_bg eq "1") { $selected1 = "selected";
	} else { $selected0 = "selected"; }
	print "<option value=\"0\" $selected0>透過しない",
	"<option value=\"1\" $selected1>透過する",
	"</select></td>\n";
	print <<EOM;
</tr><tr>
<td>
<br>
<input type="submit" value="設定変更する" class="post">
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
<input type="submit" value="設定を初期化する" class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  カラーモード保存
#-------------------------------------------------
sub save_cmode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	open(OUT,">$colorfile") || &error("カラーデータファイル $colorfile を正しく更新できませんでした。");
	print OUT "$in{'colormode'}";
	close(OUT);

	# 表示モード設定
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  カラーモード設定変更
#-------------------------------------------------
sub change_color {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	open(PARA,"$colordata") || &error("カラーデータファイル $colordata がありません。");
	@para = <PARA>;
	close(PARA);

	$para[$in{'colormode'}] = "$in{'bgcolor'}<>$in{'text'}<>$in{'cntCol'}<>$in{'tCol'}<>$in{'tblCol'}<>$in{'tbl_col0'}<>$in{'thr_brd'}<>$in{'menu_chr'}<>$in{'menu_bg'}<>$in{'menu_solid'}<>$in{'menu_brd'}<>$in{'allt_col'}<>$in{'allt_solid'}<>$in{'allt_brd'}<>$in{'tbl_col1'}<>$in{'tarea_brd'}<>$in{'btn_col'}<>$in{'btx_col'}<>$in{'btn_solid'}<>$in{'btn_brd'}<>$in{'formCol1'}<>$in{'formCol2'}<>$in{'post_chr'}<>$in{'post_bg'}<>$in{'post_solid'}<>$in{'post_brd'}<>$in{'moji_col'}<>$in{'back_col'}<>$in{'radio_brd'}<>$in{'border'}<>$in{'cellspacing'}<>$in{'cellpadding'}<>$in{'topmark'}<>$in{'comark'}<>$in{'margin_left'}<>$in{'margin_right'}<>$in{'subCol'}<>$in{'sub_len'}<>$in{'frm_brd'}<>$in{'frm_bc'}<>$in{'frm_tx'}<>$in{'frm_solid'}<>$in{'refcol'}<>$in{'tree_bc'}<>$in{'scroll'}<>$in{'thr_bg'}<>$in{'lheight'}<>$in{'width'}<>\n";


	# 設定ファイルを保存
	open(OUT,">$colordata") || &error("カラーデータファイル $colordata を正しく更新できませんでした。");
	print OUT @para;
	close(OUT);

	# 表示モード設定
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  カラーモード設定初期化
#-------------------------------------------------
sub color_clear {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	unlink("$colordata");
	rename($colorinit,$colordata) || &error("カラー設定ファイルエラー");

	open(PARA,"$colordata");
	@para = <PARA>;
	close(PARA);

	open(COL,">$colorinit");
	print COL @para;
	close(COL);

	open(OUT,">$colorfile");
	print OUT "1";
	close(OUT);

	# 表示モード設定
	if ($boardmode && -s "$colordata") { &read_color; }
	&admin;
}

#-------------------------------------------------
#  表示形式変更
#-------------------------------------------------
sub change_mode {
	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	if ($in{'boardmode'}) {
		open(OUT,">$colorfile");
		print OUT "0";
		close(OUT);
	} else {
		open(OUT,">$colorfile");
		print OUT "1";
		close(OUT);
	}

	# 表示モード設定
	&message("表\示モードを変更しました");
}

#-------------------------------------------------
#  掲示板再開
#-------------------------------------------------
sub reopen {
	my @data = ();
	# ログ読み込み
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		push(@data,"$_");
	}

	# 更新
	seek(DAT, 0, 0);
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	&message("掲示板を再開しました");
}

#-------------------------------------------------
#  スパムログ
#-------------------------------------------------
sub spam {
	my (%reno,%date,%name,%email,%sub,%url,%msg,%host,%pwd,%color,
	%icon,%sml,%reason,%tim,%pdate,%timecheck,%useragent,%fcheck);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	my $file = $spamlogfile;
	my $job = "spam";
	if ($mode eq "error") {
		$job = "error";
		$file = $er_log;
		$postmode = "エラー";
		$alreason = "エラー理由";
	}

	&header;
	print <<EOM;
<ul>
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; 掲示板へ" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
</form>
</td></tr>
</table></div>
</ul>
<ul><li>$postmodeログ<br>
必用な$postmodeを復活させたあとは、「$postmodeログを削除」しておいて下さい。
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spamclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job"  value="$job">
<input type="submit" value=" $postmodeログを全て削除する " class="post">
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
			$fcheck{$i} = qq|アクセス記録なし|;
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

	# ソート処理
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
			"<td bgcolor=\"$tblcol\">投稿日時</td><td bgcolor=\"$tblcol\">$pdate{$_}</td>",
			"<td bgcolor=\"$tblcol\">タイトル</td><td bgcolor=\"$tblcol\">$sub{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">アクセス日時</td><td bgcolor=\"$tblcol\">$fcheck{$_}</td>",
			"<td bgcolor=\"$tblcol\">$alreason</td><td bgcolor=\"$tblcol\">$reason{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">投稿者名</td><td bgcolor=\"$tblcol\">$name{$_}</td>",
			"<td bgcolor=\"$tblcol\">URL</td><td bgcolor=\"$tblcol\">$url{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
			"<td bgcolor=\"$tblcol\">ホストアドレス</td><td bgcolor=\"$tblcol\">$host{$_}</td>",
			"<td bgcolor=\"$tblcol\">ブラウザ</td><td bgcolor=\"$tblcol\">$useragent{$_}</td></tr>",
		"<tr bgcolor=\"$tblcol\">",
		"<td bgcolor=\"$tblcol\">メールアドレス</td><td bgcolor=\"$tblcol\">$email{$_}</td>",
		"<td bgcolor=\"$tblcol\">投稿内容</td><td bgcolor=\"$tblcol\"> ";
		if ($msg{$_}) {
			print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spammsg">
<input type="hidden" name="job"  value="$job">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="msg" value="$msg{$_}">
<input type="submit" value="投稿内容を閲覧" class="post">
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
<input type="submit" value="再投稿処理" class="post">
</form></td><td>(上記の投稿を復活させることができます)</td></tr></table>
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
		print "<input type=\"submit\" value=\"前画面\"></form></td>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$admincgi\" method=\"$method\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"$in{'mode'}\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$next\">\n";
		print "<input type=\"submit\" value=\"次画面\"></form></td>\n";
	}
	print "</tr></table>\n";
	print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="spamclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job"  value="$job">
<input type="submit" value=" $postmodeログを全て削除する " class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  投稿拒否ログ初期化
#-------------------------------------------------
sub spamclear {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	my $file = $spamlogfile;
	if ($in{'job'} eq "error") {
		$file = $er_log;
		$postmode = "エラー";
	}

	# 投稿拒否ログの初期化
	open(CL,"+>$file");
	close(CL);

	&header();
	print <<EOM;
<div align="center">
<h4>$postmodeログを削除しました</h4>
<table border="0">
<tr><td><form action="$bbscgi">
<input type="submit" value="&lt; 掲示板へ" class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
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
#  投稿拒否コメント
#-------------------------------------------------
sub spammsg {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	if ($in{'job'} eq "error") {
		$postmode = "エラー";
	}

	# エスケープ
	$in{'msg'} =~ s/"/&quot;/g;
	$in{'msg'} =~ s/</&lt;/g;
	$in{'msg'} =~ s/>/&gt;/g;
	# 改行処理
	$in{'msg'} =~ s/&lt;br&gt;/<br>/ig;

	&header();
	print <<EOM;
<div align="center">
<h4>コメント</h4>
<p><table border="0" cellspacing="0" cellpadding="0">
<tr bgcolor="$tbl_col0">
<td bgcolor="$tbl_col0">
<table border="$border" cellspacing="1" cellpadding="5">
<tr bgcolor="$tblcol">
<td bgcolor="$tblcol"><div align="center">
$postmode メッセージ内容</div></td></tr>
<tr bgcolor="$tblcol">
<td bgcolor="$tblcol">$in{'msg'}</td></tr>
</table>
</td></tr>
</table><br>
<table border="0">
<tr><td><form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="$in{'job'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" $postmodeログ閲覧に戻る " class="menu">
</form>
</td><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
</form>
</td></tr>
</table></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  NGワード編集
#-------------------------------------------------
sub spamdata {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	&header;
	print <<EOM;
<div align="left">
<table border="0">
<tr><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
</form>
</td></tr>
</table></div>
<br>
<li>NGワードを一括登録できます(半角のカンマで区切る)。<br>
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
<input type="submit" value="更新する" class="post">
</form>
</ul>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  NGワード更新
#-------------------------------------------------
sub editspam {

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	$SPMLST = $in{"SPMLST"};

	# 空データ・改行・空白を削除
	$SPMLST =~ s/，/\,/g;
	$SPMLST =~ s/<br>//ig;
	$SPMLST =~ s/<br>//ig;
	$SPMLST =~ s/\n//g;
	$SPMLST =~ s/\r//g;
	$SPMLST =~ s/　//g;
	$SPMLST =~ s/\,{2,}/\,/g;
	$SPMLST =~ s/^\,{1,}//;

	open(OUT,">$spamdata") || &error("Write Error");
	print OUT $SPMLST;
	close(OUT);

	&header;

	print <<EOM;
<div align="center">
<h4>NGワードを更新しました</h4>
<br>
<table border="0">
<tr><td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
</form>
</td></tr>
</table></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  管理者再投稿画面
#-------------------------------------------------
sub admin_repost_form {

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	if ($in{'job'} eq "error") {
		$postmode = "エラー";
		$alreason = "エラー理由";
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
<h3>$postmodeとして処理された下記の投稿を復活させます。</h3>
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
  <td><b>お名前</b>&nbsp;:&nbsp;
    <input type="text" name="name" value="$in{'name'}" size="28" class="f"></td>
</tr>
<tr>
  <td><b>Ｅメール</b>&nbsp;:&nbsp;
    <input type="text" name="email" size="36" value="$in{'email'}"></td>
</tr>
<tr>
  <td><b>ＵＲＬ</b>&nbsp;:&nbsp;
  <input type="text" name="url" size="50" value="$in{'url'}" class="f"></td>
</tr>
<tr>
  <td><b>タイトル</b>&nbsp;:&nbsp;
    <input type="text" name="sub" size="36" value="$in{'sub'}" class="f">
  </td>
</tr>
<tr>
  <td>
    <b>メッセージ</b><br>
    <textarea cols="56" rows="7" name="comment" wrap="soft" class="f">$in{'msg'}</textarea>
  </td>
</tr>
</table>
<table><tr><td>
<input type="submit" value="投稿復活処理する" class="post">
</form>
</td>
<form action="$admincgi" method="$method">
<td><input type="hidden" name="mode" value="$in{'job'}">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" $postmodeログ閲覧に戻る " class="post">
</form>
</td></tr></table>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  Webmail送信ログ
#-------------------------------------------------
sub sendmaillog {
	my (%dat,%nam,%em,%to,%sem,%hos,%no,%date);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	&header;
	print <<EOM;
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理画面に戻る " class="menu">
</form>
<li>Webmail送信ログ
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="maillogclear">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 送信記録を削除する " class="post">
</form>
<p>Webmailを利用したメール送信記録です。</p>
<table border="1">\n<tr><td>日時</td><td>送信者名</td><td>送信者メールアドレス</td>
<td>送信元ホストアドレス</td><td>受信者名</td><td>受信者メールアドレス</td><td>記事No</td></tr>
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
<input type="submit" value=" 送信記録を削除する " class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  送信記録を削除
#-------------------------------------------------
sub maillogclear {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'pass'} eq "") { &enter; }
	elsif ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	unlink("$mailchk$sendmaillog");

	&header;
	print <<EOM;
<li>Webmail送信ログを削除しました。</li>
<br>
<br>
<table><tr><td>
<form action="$bbscgi" method="$method">
<input type="hidden" name="page" value="$page">
<input type="submit" value="&lt; 掲示板へ" class="menu">
</form>
</td>
<td>
<form action="$admincgi" method="$method">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value=" 管理モードに戻る " class="menu">
</form>
</tr></table>
</body>
</html>
EOM
	exit;
}


__END__


