#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ regist.cgi - 2006/10/09
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
&axsCheck;
($mode,$timecheck) = &previewcheck;

# 自動閉鎖
if ($clday) {
	my $last = (stat $logfile)[9];
	if (abs(time - $last) > $clday*24*3600) {
		&header;
		&pseudo;
		&autoclose;
	}
}

if ($mode eq "dele") { require $editlogpl; &dele; }
elsif ($mode eq "edit") { require $editlogpl; &edit; }
elsif ($mode eq "$writevalue" && $in{'pview'} ne "on") { &regist; }
elsif ($mode eq "$postvalue" && $in{'pview'} eq "on") { &regist; }
elsif ($mode eq "$writevalue" && $in{'pview'} eq "on") { &error("$spammsg"); }
elsif ($mode eq "previewmode") { &previewmode("$timecheck"); }
elsif ($in{'pass'} eq $pass && $mode eq "admin_repost") { &regist; }
elsif ($mode eq "regist" || $mode eq "write") { &message("投稿処理を中止しました。"); }
&error("不明な処理です。");

#-------------------------------------------------
#  記事登録
#-------------------------------------------------
sub regist {
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	# 時間取得
	&get_time;

	# フォーム入力チェック
	@col = split(/\s+/, $color);
	if ($mode ne "admin_repost") { &formCheck; }

	# 管理者詐称チェック
	my $acflag = 0;
	foreach (split(/\,/, $AdminName)) {
		if ($in{'name'} =~ /\Q$_\E/i) { $acflag=1; last; }
	}
	if ($adminchk && $acflag) { &error("$in{'name'}を名乗ることはできません。"); }

	# 管理者チェック
	my $aflag = 0;
	if ($in{'name'} eq $admin_id && $in{'pwd'} eq $pass) {
		$ccolor = $in{'color'}; @color = split(/\s+/, $color); $acol = $#color+1;
		$in{'color'} = $acol; $col[$acol] = $a_color;
		$in{'name'} = $a_name; $aflag = 1;
	}

	# 投稿キーチェック
	if ($regist_key && $mode ne "admin_repost") {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("投稿キーが入力不備です。<p>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}

		# 投稿キーチェック
		# -1 : キー不一致
		#  0 : 制限時間オーバー
		#  1 : キー一致
		local($chk) = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("投稿キーが制限時間を超過しました。<p>投稿フォームに戻って再読込み後、指定の数字を再入力してください");
		} elsif ($chk == -1) {
			&error("投稿キーが不正です。<p>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}
	}

	# ログを開く
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;

	# 記事NO処理
	local($no,$ip,$tim) = split(/<>/, $top);
	$no++;

	# 連続投稿チェック
	my $flg = 0;
	if ($mode ne "admin_repost") {
		if ($regCtl == 1) {
			if ($addr eq $ip && $times - $tim < $wait) { $flg = 1; }
		} elsif ($regCtl == 2) {
			if ($times - $tim < $wait) { $flg = 1; }
		}
		if ($flg) {
			close(DAT);
			&error("現在投稿制限中です。もうしばらくたってから投稿をお願いします");
		}
	}

	# 改行・ダブルクオート復元
	if ($in{'pview'} eq "on") {
		$in{'comment'} =~ s/&lt;br&gt;/<br>/g;
		$in{'comment'} =~ s/&quot;/"/g;
	}

	# 重複チェック
	my $flg = 0;
	while (<DAT>) {
		my ($no2,$re,$dat,$nam,$eml,$sub,$com) = split(/<>/);

		if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
			$flg = 1;
			last;
		}
	}
	if ($flg) {
		close(DAT);
		&error("重複投稿のため処理を中断しました");
	}

	# 巻き戻し
	seek(DAT, 0, 0);
	$top = <DAT>;

	# 削除キーを暗号化
	if ($mode ne "admin_repost") {
		if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }
	}

	# スパム投稿チェック
	($spam,$reason) = &spam_check($in{'name'},$in{'url2'},$in{"$bbscheckmode"},$in{'comment'},
	$in{'reno'},$in{'url'},$in{'email'},$in{'sub'},$in{'mail'},$in{"$formcheck"},$cnam,$in{'submit'},
	$in{'subject'},$in{'title'},$in{'theme'},$ENV{'HTTP_ACCEPT_LANGUAGE'},$ENV{'HTTP_USER_AGENT'});

	# プレビュー＆スパムログの削除
	if ($in{'pview'} eq "on" || $mode eq "admin_repost") {
		if ($spamlog) { &del_spamlog("$in{\"$bbscheckmode\"}","spam"); }
	}
	# エラーログの削除
	if ($errtime) { &del_spamlog("$in{\"$bbscheckmode\"}","error"); }

	# スパム投稿処理
	if ($spam && $mode ne "admin_repost") {
		close(DAT);
		# 投稿拒否ログの記録
		if ($spamlog && !$allowmode) { &write_spamlog("$reason","spam"); }
		if ($spamresult) {
			# エラー表示
			if ($spammsg) {
				if ($spamresult == 1)  { &error("$spammsg","1"); }
				else { sleep($spamresult); &error("$spammsg","1"); }
			}
		}
		# Internal Server Error
		&cgi_error;
	}

	# 復活処理
	if ($mode eq "admin_repost") {
		$date= $in{'date'};
		$host= $in{'host'};
		$pwd = $in{'pwd'};
		$times= $in{'tim'};
	}

	# 投稿制限
	if ($mode ne "admin_repost") {
		my $result = &post_check;
		if ($result) {
			close(DAT);
			&write_spamlog("$result","spam");
			&message("$denymsg");
		}
	}

	# クッキー発行
	if ($mode ne "admin_repost") {
		if ($aflag) {
			if ($no_email == 2) { $in{'email'} =~ s/\@/＠/; }
			&set_cookie($admin_id,$in{'email'},$in{'url'},$in{'pwd'},
			$in{'icon'},$ccolor,$in{'smail'},$in{'aikotoba'},$in{'refmode'});
			if ($no_email == 2) { $in{'email'} =~ s/＠/\@/; }
		} else {
			if ($no_email == 2) { $in{'email'} =~ s/\@/＠/; }
			&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'},
			$in{'icon'},$in{'color'},$in{'smail'},$in{'aikotoba'},$in{'refmode'});
			if ($no_email == 2) { $in{'email'} =~ s/＠/\@/; }
		}
	}

	# 投稿非公開処理
	my (@lines,@spampost);
	if (!$aflag && $allowmode && $mode ne "admin_repost") {
		close(DAT);
		# 非公開ログファイル読み込み
		open(SPLOG,"$spamlogfile") || &error("ログファイル $spamlogfile がありません。");
		@lines = <SPLOG>;
		close(SPLOG);

		# 二重投稿のチェック
		my $flag = 0;
		foreach (@lines) {
			@spampost = split(/<>/);
			if ($in{'comment'} eq $spampost[6]) { $flag = 1; last; }
			# 連続投稿チェック
			if ($host eq $spampost[8] && $wait > $times - $spampost[12]) {
				&error("もうしばらく時間をおいてから投稿して下さい");
			}
		}
		if ($flag) { &error("二重投稿は禁止です"); }

		&write_spamlog("$reason","spam");
		# メール通知
		if ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }
		elsif ($mailing == 2) { &mail_to; }
		&message("$spammsg");
	}

	# sage
	if ($in{'sage'}) {
		$topsort = 0;
	}

	# 親記事の場合
	if ($in{'reno'} eq "") {

		my $i = 0;
		my $stop = 0;
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);
			$i++;
			if ($i > $max-1 && $reno2 eq "") { $stop = 1; }
			if (!$stop) { push(@new,$_); }
			elsif ($stop && $pastkey) { push(@data,$_); }
		}
		unshift(@new,"$no<><>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
		if ($mode ne "admin_repost") {
			unshift(@new,"$no<>$addr<>$times<>\n");
		} else {
			unshift(@new,"$no<>$ip<>$tim<>\n");
		}

		# 過去ログ更新
		if (@data > 0) { &pastlog(@data); }

		# 更新
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# レス記事の場合：トップソートあり
	} elsif ($in{'reno'} && $topsort) {

		my ($f,$oyaChk,$match,@new,@tmp);
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);

			if ($in{'reno'} == $no2) {
				if ($reno2) { $f++; last; }
				$oyaChk++;
				$match=1;
				push(@new,$_);

			} elsif ($in{'reno'} == $reno2) {
				push(@new,$_);

			} elsif ($match == 1 && $in{'reno'} != $reno2) {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
				push(@tmp,$_);

			} else { push(@tmp,$_); }
		}
		if ($f) {
			close(DAT);
			close(DAT);&error("不正な返信要求です");
		}
		if (!$oyaChk) {
			close(DAT);
			&error("親記事が存在しません");
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
		}
		push(@new,@tmp);

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# レス記事の場合：トップソートなし
	} else {

		my ($f,$oyaChk,$match,@new);
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);

			if ($in{'reno'} == $no2) { $oyaChk++; }
			if ($match == 0 && $in{'reno'} == $no2) {
				if ($reno2) { $f++; last; }
				$match = 1;

			} elsif ($match == 1 && $in{'reno'} != $reno2) {
				$match = 2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
			}
			push(@new,$_);
		}
		if ($f) {
			close(DAT);
			&error("不正な返信要求です");
		}
		if (!$oyaChk) {
			close(DAT);
			&error("親記事が存在しません");
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>\n");
		}

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	if ($mode ne "admin_repost") {
		# メール処理
		if ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }
		elsif ($mailing == 2) { &mail_to; }
	}

	# リロード
	if ($location) {
		if ($ENV{'PERLXS'} eq "PerlIS") {
			print "HTTP/1.0 302 Temporary Redirection\r\n";
			print "content-type: text/html\n";
		}
		print "Location: $location?list=$in{'list'}\n\n";
		exit;

	} else {
		&message('投稿は正常に処理されました');
	}
}

#-------------------------------------------------
#  入力確認
#-------------------------------------------------
sub formCheck {
	local($task) = @_;
	local($ref);

	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	# 投稿時
	if ($task ne "edit") {
		# 他サイトからのアクセス排除
		if ($baseUrl) {
			$ref = $ENV{'HTTP_REFERER'};
			$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
			$baseUrl =~ s/(\W)/\\$1/g;
			if ($ref && $ref !~ /$baseUrl/i) { &error("不正なアクセスです"); }
		}

		# 拡張オプションチェック
		&option_check($in{'pwd'},$in{'email'},$in{'message'},$in{'url'});
		if ($in{'email'} && $in{'email'} =~ /＠/) { $in{'email'} =~ s/＠/\@/; }

		if ($aikotoba) {
			if ($in{'aikotoba'} ne $aikotoba) { &error("合い言葉が不正です"); }
		}
	}

	# 名前とコメントは必須
	if ($in{'name'} eq "") { &error("名前が入力されていません"); }
	if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
	if (!$in{'email'}) { $in{'smail'} = 0; }
	if ($in_email && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("Ｅメールの入力内容が正しくありません");
	}
	if (!$in_email && $in{'email'}) {
		if ($in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
			&error("Ｅメールの入力内容が正しくありません");
		}
	}

	if ($iconMode) {
		@ico1 = split(/\s+/, $ico1);
		@ico2 = split(/\s+/, $ico2);
		if ($my_icon) { push(@ico1,$my_gif); }
		if ($in{'icon'} =~ /\D/ || $in{'icon'} < 0 || $in{'icon'} > @ico1) {
			&error("アイコン情報が不正です");
		}
		$in{'icon'} = $ico1[$in{'icon'}];

		# 管理アイコンチェック
		if ($my_icon && $in{'icon'} eq $my_gif && $in{'pwd'} ne $pass) {
			&error("管理用アイコンは管理者専用です");
		}
	}

	@col = split(/\s+/, $color);
	if ($in{'color'} =~ /\D/ || $in{'color'} < 0 || $in{'color'} > @col) {
		&error("文字色情報が不正です");
	}

	# emailチェック
	if ($in{'email'}) {
		my $atmark = $in{'email'} =~ s/\@/\@/g;
		if ($atmark != 1) {
			&error("Ｅメールの入力が不正です");
		}
	}

	# URL
	if ($in{'url'} && $in{'url'} !~ /^https?\:\/\//i) { &error("URLの入力が不正です"); }
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }

	# 機種依存文字チェック
	$pdcnam = &find_mdc( $in{'name'}, $pdch, $pdcf );
	if($pdcnam) { &error("$pdcerror『&nbsp;$pdcnam&nbsp;』"); }
	$pdcsub = &find_mdc( $in{'sub'}, $pdch, $pdcf );
	if($pdcsub) { &error("$pdcerror『&nbsp;$pdcsub&nbsp;』"); }
	$pdcmsg = &find_mdc( $in{'comment'}, $pdch, $pdcf );
	if($pdcmsg) { &error("$pdcerror<br><br><table border=1><tr><td>$pdcmsg</td></tr></table>"); }

	# タイトルチェック
	if (!$in{'sub'}) {
		if ($suberror) { &error("タイトルが入力されていません"); } else { $in{'sub'} = "無題"; } 
	} elsif ($suberror == 2) {
		if ($in{'sub'} !~ /[^0-9]/ || $in{'sub'} =~ /http\:\/\//i) { &error("タイトルが不正です"); }
	}

	# 引用だけ・引用が多い投稿の禁止
	$cflg = 0; $rowa = 0; $rowb = 0;
	$message = $in{'comment'};
	$message =~ s/&lt;br&gt;/<br>/g;
	@message = split(/<br>/i,$message);
	foreach(@message){
		if ($_ =~ /^>/ || $_ =~ /^&gt;/) {
			# 引用文字数をカウント
			$rowa = $rowa+length($_); next;
			# メッセージ文字数をカウント
		} elsif($_) { $rowb = $rowb+length($_); $cflg = 1;} 
	}
	if (!$cflg) { &error("引用が多すぎるかコメントがありません"); }
	if ($mode ne "admin_repost" && $rrate) {
		if ($rowa/$rowb >= $rrate) { &error("引用部分が多すぎます"); }
	}

	# 非公開チェック
	if ($in{'smail'}) {
		if ($in{'smail'} ne "1") { &error("選択が正しくありません。");}
	}
}

#-------------------------------------------------
#  機種依存文字検出  
#-------------------------------------------------
# 機種依存文字検出＋ハイライト表示追加関数
# Check platform dependent characters / Thanks to carmine
# [Usage] $result = &find_mdc( $buf, '<font color="red">', '</font>' );
sub find_mdc {
	local( $buf, $prefix, $postfix ) = @_;
	local( $len, $c1, $c2, $o1, $o2, $i, $k, $pdc, $result );

	$k = 0;
	$pdc = 0;
	$result = "";
	$len = length( $buf );
	for( $i = 0; $i < $len; ++$i ){
		if( $k ){
			$k = 0;
			$c2 = substr( $buf, $i, 1 );
			$o2 = ord( $c2 );
			if( ( $o1 >= 0x85 && $o1 <= 0x88 ) && ( $o2 >= 0x40 && $o2 <= 0x9e ) ){
				$result .= $prefix . $c1 . $c2 . $postfix;
				$pdc = 1;
			} else {
				$result .= $c1 . $c2;
			}
			$k = 0;
		} else {
			$c1 = substr( $buf, $i, 1 );
			$o1 = ord( $c1 );
			if( ( $o1 > 0x80 && $o1 <= 0x9F ) || ( $o1 >= 0xE0 && $o1 <= 0xFC ) ){
				$k = 1;
			} else {
				$result .= $c1;
			}
		}
	}
	if ($pdc) { return $result; } else {return $pdc; }
}

#-------------------------------------------------
#  メール送信
#-------------------------------------------------
sub mail_to {
	# 記事の改行・タグを復元
	my $com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	my $ptn = 'https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$ptn" target="_blank">($ptn)<\/a>/$1/go;
	$com =~ s/&lt;/＜/g;
	$com =~ s/&gt;/＞/g;
	$com =~ s/&quot;/”/g;
	$com =~ s/&amp;/＆/g;

	# メール本文を定義
	my $agent = &escape($ENV{'HTTP_USER_AGENT'});
	my $mbody = <<EOM;
投稿日時：$date
ホスト名：$host
ブラウザ：$agent

投稿者名：$in{'name'}
Ｅメール：$in{'email'}
参照先  ：$in{'url'}
タイトル：$in{'sub'}

$com
EOM

	# 題名をBASE64化
	my $msub = &base64("$title (No.$no)");

	# コード変換
	&jcode::convert(\$mbody, 'jis', 'sjis');

	# メールアドレスがない場合は管理者アドレスに置き換え
	 my $email = $in{'email'};
	 if ($in{'email'} eq "") { $email = $mailto; }

	open(MAIL,"| $sendmail -t -i") || &error("メール送信失敗");
	print MAIL "To: $mailto\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=iso-2022-jp\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "--------------------------------------------------------\n";
	print MAIL "$mbody\n";
	print MAIL "--------------------------------------------------------\n";
	close(MAIL);
}

#-------------------------------------------------
#  BASE64変換
#-------------------------------------------------
#		とほほのWWW入門で公開されているルーチンを
#		参考にしました。( http://tohoho.wakusei.ne.jp/ )
sub base64 {
	my $sub = shift;
	&jcode::convert(\$sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i = 0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  過去ログ生成
#-------------------------------------------------
sub pastlog {
	local(@data) = @_;

	# 過去ログNoファイル
	open(NO,"+< $nofile") || &error("Open Error: $nofile");
	eval "flock(NO, 2)";
	my $count = <NO>;

	# 過去ログ定義
	my $pastfile = sprintf("%s/%04d.cgi", $pastdir,$count);

	# 過去ログオープン
	my $i = 0;
	my ($flg, @past);
	open(PF,"+< $pastfile") || &error("Open Error: $pastfile");
	eval "flock(PF, 2)";
	while (<PF>) {
		$i++;
		push(@past,$_);
		if ($i >= $pastmax) { $flg++; last; }
	}

	# 規定の行数をオーバーすると次ファイルを自動生成
	if ($flg) {

		# カウントファイル更新
		seek(NO, 0, 0);
		print NO ++$count;
		truncate(NO, tell(NO));

		close(PF);

		# 新過去ログ
		$pastfile = sprintf("%s/%04d.cgi", $pastdir,$count);
		@past = @data;

		open(PF,"> $pastfile") || &error("Open Error: $pastfile");
		print PF @past;
		close(PF);

	} else {
		unshift(@past,@data);

		# 過去ログ更新
		seek(PF, 0, 0);
		print PF @past;
		truncate(PF, tell(PF));
		close(PF);
	}

	close(NO);

	# 新規生成の場合パーミッション変更
	if ($flg) { chmod(0666, $pastfile); }
}

#-------------------------------------------------
#  禁止ワードチェック
#-------------------------------------------------
sub no_wd {
	local($flg);
	foreach ( split(/,/, $no_wd) ) {
		if (index("$in{'name'} $in{'sub'} $in{'comment'}",$_) >= 0) {
			$flg = 1; last;
		}
	}
	if ($flg) { &error("禁止ワードが含まれています"); }
}

#-------------------------------------------------
#  日本語チェック
#-------------------------------------------------
sub jp_wd {
	local($sub, $com, $mat1, $mat2, $code1, $code2);
	$sub = $in{'sub'};
	$com = $in{'comment'};
	if ($sub) {
		($mat1, $code1) = &jcode'getcode(*sub);
	}
	($mat2, $code2) = &jcode'getcode(*com);
	if ($code1 ne 'sjis' && $code2 ne 'sjis') {
		&error("題名又はコメントに日本語が含まれていません");
	}
}

#-------------------------------------------------
#  URL個数チェック
#-------------------------------------------------
sub urlnum {
	local($com) = $in{'comment'};
	local($num) = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("コメント中のURLアドレスは最大$urlnum個までです");
	}
}

#-------------------------------------------------
#  スパム拡張オプションチェック
#-------------------------------------------------
sub option_check {
	my ($pw,$em,$cm,$ur) = @_;

	# 削除キーをチェック
	my $flag = 0;
	if ($ng_pass && $pw) {
		if ($pw =~ /\s/ || $pw eq reverse($pw)) {
			$flag = 1;
		}
	}
	if ($flag) {
		&error("削除キーが不正です。");
	}

	# メールアドレスをチェック
	if ($no_email == 1 && $em) {
		&error("メールアドレスは入力禁止です。");
	}
	if ($no_email == 2 && $em && $em !~ /^[\w\.\-]+＠[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("アットマーク ＠ は全角で入力して下さい。"); 
	}

	# URLの直接書き込みをチェック
	if ($comment_url) { 
		my $ulnum = ($cm =~ s/http/http/ig);
		if ($ulnum) {
			&error("ＵＲＬは先頭のｈを抜いて書き込んで下さい。");
		}
	}

	# URL転送・短縮URLをチェック
	my $shorturlcheck = 0;
	if ($shorturl) { 
		if ($cm =~ /https?\:\/\/[\w\-]{1,10}?\.[\w\-]{2,5}?\//i || 
			$ur =~ /https?\:\/\/[\w\-]{1,10}?\.[\w\-]{2,5}?\//i) {
			my $html = $';
			if ($html =~ /^[\w\?]+?/)  {
				if ($html !~ /^index\.htm/i) {
					$shorturlcheck = 1;
				}
			}
		}
		if (!$shorturlcheck) {
			if ($cm =~ /https?\:\/\/([\w\-]{1,5}\.)?(\d+)\.[a-z]{2,4}\/?/i || 
				$ur =~ /https?\:\/\/([\w\-]{1,5}\.)?(\d+)\.[a-z]{2,4}\/?/i)
				{ $shorturlcheck = 2; }
		}
		if ($shorturlcheck) {
			&error("URLの記載は禁止されています。");
		}
	}
}

#-------------------------------------------------
#  スパムチェック
#-------------------------------------------------
sub spam_check{
	my ($na,$u2,$bt,$cm,$re,$ur,$em,$sb,$ad,$fc,$cn,$smt,$sb2,$sb3,$sb4,$lng,$ua) = @_;
	my $spam = 0;
	my $reason = "公開許可待ち";
	my $tcheck = abs(time - $bt);

	if (!$spam) {
		if($ipcheckmode) {
			my $enadr = &encode_addr($addr);
			if ($ad ne $enadr) {
				$spam = 1;
				$reason = "プログラム投稿(IP不一致)";
			}
		} else {
			if ($ad =~ /\@/) {
				$spam = 1;
				$reason = "プログラム投稿(IPデータ不正)";
			}
		}
	}

	if (!$spam) {
		if (!$cn || !$cookiecheck) {
			if ($maxtime && $tcheck > $maxtime) {
				$spam = 1;
				$reason = "プログラム投稿(投稿まで$tcheck秒)";
			}
		}
	}

	# 携帯除外
	if ($keitaicheck == 1 && $keitai ne 'p') { $spam = 0; }

	if (!$spam) {
		if (!$smt) {
			$spam = 1;
			$reason = "プログラム投稿(投稿ボタン非使用)";
		}
	}

	if (!$spam) {
		if ($u2 || $sb2 || $sb3 || $sb4) {
			$spam = 1;
			$reason = "プログラム投稿(非ブラウザ)";
		}
	}

	if (!$spam) {
		if (!$bt || !$fc || !$ad) {
			$spam = 1;
			$reason = "プログラム投稿(非フォーム投稿)";
		}
	}

	if (!$spam) {
		if ($mintime && $tcheck < $mintime) {
			if ($cn && $cookiecheck) {
				&error("恐れ入りますが、一度戻ってから再投稿してください。");
			}
			$spam = 1;
			$reason = "プログラム投稿(投稿まで$tcheck秒)";
		}
	}

	# 携帯除外II
	if (!$keitaicheck && $keitai ne 'p') { $spam = 0; }

	# 携帯からのURL記入チェック
	if (!$spam) {
		if($keitaiurl && $keitai ne 'p') {
			if ($cm =~ /http/i || $ur) {
				&error("URLは書き込まないでください。");
			}
		}
	}

	if (!$spam) {
		if ($em && $em =~ /https?\:\/\//) {
			$spam = 1;
			$reason = "プログラム投稿(email/URL不正)";
		}
	}

	if (!$spam) {
		if ($ur && $ur =~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
			$spam = 1;
			$reason = "プログラム投稿(email/URL不正)";
		}
	}

	if (!$spam) {
		if ($minmsg) {
			if (length($cm)*2 < length($na)) {
				&error("コメント・メッセージが短すぎます。");
			}
		}
		if ($namelen && length($na) >= $namelen) {
			&error("おなまえが不適切です。");
		}
		if ($cm eq $na) {
			&error("コメント・メッセージ内容が不適切です。");
		}
	}

	if (!$spam) {
		if ($na =~ /https?\:\/\//i) {
			$spam = 1;
			$reason = "プログラム投稿(name/comment不正)";
		}
	}

	# スパム投稿チェック(多数URL記述対応)
	if (!$spam) {
		my $ulnum = ($cm =~ s/http/http/ig);
		if ($spamurlnum && ($ulnum >= $spamurlnum)) {
			$spam = 1;
			$reason = "URLの書き込みが$ulnum個";
		}
	}

	# URL以外の文字数をチェック
	if (!$spam) {
		if ($characheck) {
			if ($cm =~ /(https?\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@\,]+)/ || $ur) {
				my $charamsg = $cm;
				$charamsg =~ s/(https?\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@\,]+)//g;
				$charamsg =~ s/[\s\n\r\t]//g;
				$charamsg =~ s/<br>//ig;
				$msgnum = length($charamsg);
				if ($msgnum < $characheck) {
					$spam = 1;
					$reason = "コメントの文字数が$msgnumバイトと少ない";
				}
			}
		}
	}

	# 日本語文チェック
	if (!$spam) {
		if ($asciicheck) {
			if ($cm !~ /(\x82[\x9F-\xF2])|(\x83[\x40-\x96])/) {
				$spam = 1;
				$reason = "コメントに日本語(ひらがな/カタカナ)がない";
			} else {
				my $flag = 0;
				foreach (@period ) {
					if ($cm =~ /$_/) {
						$flag = 1;
						last;
					}
				}
				if (!$flag) {
					$spam = 1;
					$reason = "コメントに句読点がない";
				}
			}
		}
	}

	if (!$spam) {
		if (-e $spamdata) {
			if ($spamdatacheck || !$re) {
				# 禁止URLデータをロード
				open(SPAM,"$spamdata") || &error("Open Error : $spamdata");
				eval { flock(SPAM, 1); };
				my $SPM = <SPAM>;
				close(SPAM);
				# 禁止URLの書き込みをチェック
				foreach (split(/\,/, $SPM)) {
					if(length($_) > 1) {
						if ($cm =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "名前/コメント内に禁止語句$_を含む投稿";
							last;
						}
						if (!$spam && $na =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "名前/コメント内に禁止語句$_を含む投稿";
							last;
						}
						if (!$spam && $ur =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "URLに禁止語句$_を含む投稿";
							last;
						}
						if (!$spam && $ngmail && $em =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "メールアドレスに禁止語句$_を含む投稿";
							last;
						}
						if (!$spam && $ngtitle && $sb =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "タイトルに禁止語句$_を含む投稿";
							last;
						}
					}
				}
			}
		}
	}

	if (!$spam) {
		if ($urlcheck) {
			if ($urlcheck eq 2 || !$re) {
				# URLのコメントへの重複書き込みをチェック
				if($ur) {
					$ur =~ s/\/$//;
					if ($cm =~ /\Q$ur\E/i) {
						if ($' !~ /(^\/?[\w\?]+?)/)  {
							$spam = 1;
							$reason = "コメント内にURL欄と同じURLを含む投稿";
						}
					}
				}
			}
		}
	}

	if (!$spam) {
		if (-e $spamip) {
			use Socket;
			my ($ip,$ngip,$dm,@dm);
			# 禁止URLデータをロード
			open(IP,"$spamip") || &error("Open Error : $spamip");
			eval { flock(IP, 1); };
			my $ipdata = <IP>;
			close(IP);
			# URL欄
			$ur =~ s/\/$//g;
			$ur =~ s/https?\:\/\///g;
			if ($ur =~ /[\w\-]{2,}?\.[\w\.\~\-\?\&\=\+\@\;\#\:\%\,]{2,}/) {
				eval { $ip = inet_ntoa(inet_aton($&)); };
				foreach $ngip (split(/\,/, $ipdata)){
					if ($ip =~ /^$ngip/) {
						$spam = 1;
						$reason = "URL欄に禁止URL($ur)";
						last;
					}
				}
			}
			if (!$spam) {
				# 本文
				@dm = $cm =~ /[-_a-z0-9]{3,}\.[-_\.a-z0-9]{2,}/g;
				foreach $dm (@dm){
					eval { $ip = inet_ntoa(inet_aton($dm)); };
					foreach $ngip (split(/\,/, $ipdata)){
						if ($ip =~ /^$ngip/) {
							$spam = 1;
							$reason = "コメント欄に禁止URL($dm)";
							last;
						}
					}
				}
			}
		}
	}

	return ($spam,$reason);
}

#-------------------------------------------------
#  エラー/スパムログ削除
#-------------------------------------------------
sub del_spamlog {
	my ($checktime,$job) = @_;
	my $file = $spamlogfile;
	if ($job eq "error") {
		$file = $er_log;
	}
	my @new = ();
	open(DATA,"+<$file");
	eval { flock(DATA, 2); };
	while (<DATA>) {
		my ($no,$reno,$date,$name,$email,$sub,$msg,$url,$host,$pwd,$color,$icon,$tim,$sml,
		$reason,$fcheck,$referer,$useragent,$times) = split(/<>/);
		if ($fcheck ne $checktime) {
			push(@new,"$_");
		}
	}
	seek(DATA, 0, 0);
	print DATA @new;
	truncate(DATA, tell(DATA));
	close(DATA);
}

#-------------------------------------------------
#  プレビューチェック
#-------------------------------------------------
sub previewcheck {
	$in{"$bbscheckmode"} = &decode_bbsmode($in{"$bbscheckmode"});
	if ($mode eq "$writevalue") {
		if ($previewmax || $previewmin) {
			if ($in{'pview'} ne "on") {
				$timecheck = abs(time - $in{"$bbscheckmode"});
				if ($timecheck <= $maxtime) {
					if ($previewmax) {
						if ($timecheck > $previewmax) {
							$mode = "previewmode";
						}
					}
				}
				if ($timecheck >= $mintime) {
					if ($timecheck < $previewmin) {
						$mode = "previewmode";
					}
				}
			}
		}
	}
	return ($mode,$timecheck);
}

#-------------------------------------------------
#  プレビュー画面
#-------------------------------------------------
sub previewmode {
	my $timecheck = shift;

	# チェック
	&formCheck;

	# プレビューログの記録
	my $writelog = 0;
	if ($spamlog) {
		if ($spamlog == 2) {
			# ひらがなを含む場合のみ記録
			if ($in{'comment'} =~ /(\x82[\x9F-\xF2])/) {
				$writelog = 1;
			}
		} else {
			$writelog = 1;
		}
	}
	if ($writelog) {
		&write_spamlog("プレビュー表\示後に未投稿 ($timecheck秒)","spam");
	}

	# エンコード処理
	$in{"$bbscheckmode"} = &encode_bbsmode($in{"$bbscheckmode"});

	my $iflag = 0;
	my $i = 0;
	# 管理者アイコン
	my @ico1 = split(/\s+/, $ico1);
	if ($my_icon) { push(@ico1,$my_gif); }
	# アイコン
	foreach(@ico1) {
		if ($in{'icon'} =~ /$_/) {
			$iflag = 1; $in{'icon'} = $i; last;
		}
		$i++;
	}
	if(!$iflag) { $in{'icon'} = 0; }

	my $cflag = 0;
	my $j = 0;
	foreach(split(/\s+/, $color)) {
		if ($in{'color'} =~ /\Q$_\E/) {
			$cflag = 1; $col = $j; last;
		}
		$j++;
	}
	if(!$cflag) { $col = 0; }

	# URL
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }

	&header;
	print <<EOM;
<form action="$registcgi" method="$method">
<input type="hidden" name="$bbscheckmode" value="$in{$bbscheckmode}">
<!--//
<input type="hidden" name="mode" value="write">
//-->
<input type="hidden" name="pwd" value="$in{'pwd'}">
<input type="hidden" name="name" value="$in{'name'}">
<input type="hidden" name="mail" value="$in{'mail'}">
<input type="hidden" name="email" value="$in{'email'}">
<input type="hidden" name="url" value="$in{'url'}">
<input type="hidden" name="sub" value="$in{'sub'}">
<input type="hidden" name="reno" value="$in{'reno'}">
<input type="hidden" name="icon" value="$in{'icon'}">
<input type="hidden" name="comment" value="$in{'comment'}">
<input type="hidden" name="color" value="$in{'color'}">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="num" value="$in{'num'}">
<input type="hidden" name="pview" value="on">
<input type="hidden" name="smail" value="$in{'smail'}">
<input type="hidden" name="sage" value="$in{'sage'}">
<input type="hidden" name="$formcheck" value="$in{$formcheck}">
<input type="hidden" name="aikotoba" value="$in{'aikotoba'}">
<input type="hidden" name="refmode" value="$in{'refmode'}">
<input type="hidden" name="regikey" value="$in{'regikey'}">
<input type="hidden" name="str_crypt" value="$in{'str_crypt'}">
EOM
	$in{'name'} =~ s/"/&quot;/g;
	$in{'sub'}  =~ s/"/&quot;/g;
	$in{'comment'} =~ s/"/&quot;/g;

	# ラジオボタン選択
	my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	my $cm = $in{'comment'};
	my $ur = $in{'url'};
	my $em = $in{'email'};
	my $pflg = 0;

	# 日本語チェック
	my $checked0 = "";
	my $checked1 = "checked";
	my $checked2 = "";
	if ($cm =~ /(\x82[\x9F-\xF2])/) {
		$checked0 = "checked"; $checked1 = ""; $checked2 = "";

		# 句読点チェック
		foreach (@period ) { if ($cm =~ /$_/) {$pflg = 1; last;} }
		if (!$pflg) { $checked0 = ""; $checked1 = ""; $checked2 = ""; }

		# URL重複チェック
		$ur =~ s/\/$//;
		$em =~ s/\/$//;
		if (($ur && $cm =~ /\Q$ur\E/i) ||
			($em && $cm =~ /\Q$em\E/i)) {
			if ($' !~ /(^\/?[\w\?]+?)/)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}

		# URL欄入力チェック
		if ($ur)  {
			if (!$curl)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}

		# コメント欄URLチェック
		my $urlcnt = ($cm =~ s/http/http/ig);
		if ($urlcnt)  {
			if (!$cnam)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}
	}

	if ($keitai eq 'p') {
		print <<EOM;
<div align="center">
<h1 style="color:#ff0000; background-color:#ffffff; border-top-style:solid; border-bottom-style:solid; border-color:#ff0000; border-width:1; padding-top: 5px; padding-bottom: 5px;">投稿はまだ完了しておりません。</h1>
<br>
▼ 内容を確認し、<b style="color:#ff0000">投稿する</b>をチェックして投稿を実行して下さい。<br>
<br>
<table border="1" width="90%" cellspacing="0" cellpadding="10">
<tr><td bgcolor="$tblcol">
<table>
<tr>
  <td><b>お名前</b></td>
  <td>$in{'name'}</td>
</tr>
<tr>
  <td><b>Ｅメール</b></td>
  <td>$in{'email'}</td>
</tr>
<tr>
  <td><b>タイトル</b></td>
  <td>$in{'sub'}</td>
</tr>
<tr>
  <td><b>ＵＲＬ</b></td>
  <td>$in{'url'}</td>
</tr>
<tr>
  <td><b>メッセージ</b></td>
  <td></td>
</tr>
</table>
<blockquote>
<table cellspacing="10">
<tr>
<td valign="top">$in{'comment'}</td>
</tr></blockquote>
</table>
</table>
<p>
<table cellpadding="5">
<tr>
  <td colspan="2">
  <script type="text/javascript">
  <!-- //
  fcheck("me='mode' va","<inpu","t type='radio' na","lue='$postvalue' class='radio' $checked0>");
  // -->
  </script>
  <noscript><input type="radio" name="mode" value="$postvalue"></noscript>
  <b style="color:#ff0000">投稿する</b>
  &nbsp;&nbsp;&nbsp;
  <input type="radio" name="mode" value="regist" class="radio" $checked1><small>投稿キャンセル</small>
  &nbsp;&nbsp;&nbsp;
  <input type="radio" name="mode" value="write" class="radio" $checked2><small>投稿中止</small>
  </td>
</tr>
<tr>
  <td><div align="right">
   <input type="submit" name="submit" value="   実    行   " class="post">
   </form></div></td>
   <td><form><div align="left">
     <input type="button" value="前画面に戻る" onclick="history.back()">
     </div></form>
  </td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	  } else {
		print <<EOM;
▼ 内容を確認し、投稿を実行して下さい。
<hr>
おなまえ: 
<b style='color:#0000FF'>$in{'name'}</b><br>
題名: 
<b style='color:#0000FF'>$in{'sub'}</b><br>
Ｅメール: 
<b style='color:#0000FF'>$in{'email'}</b><br>
コメント<br>
<b style='color:#0000FF'>$in{'comment'}</b><br>
<hr>
<input type="radio" name="mode" value="$postvalue" $checked0>投稿する
<br>
<input type="radio" name="mode" value="regist"s $checked1><small>投稿をやめる</small>
<br>
<input type="submit" name="submit" value="   実    行   " class="post">
</form>
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
EOM
	}
	exit;
}

#-------------------------------------------------
#  投稿制限
#-------------------------------------------------
sub post_check {
	my $result = "";
	my $flg = 0;

	# IPチェック
	foreach ( split(/\,/, $daddr) ) {
		s/\./\\\./g;
		s/\*/\.\*/g;
		if ($addr =~ /^$_/i) {
			$flg = 1;
			$result = "投稿制限IPアドレスからの投稿";
			last;
		}
	}
	if (!$flg) {
		# hostチェック
		foreach ( split(/\,/, $dhost) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;
			if ($host =~ /$_$/i) {
				$flg = 1;
				$result = "投稿制限ホストアドレスからの投稿";
				last;
			}
		}
	}
	return $result;
}

__END__

