#┌─────────────────────────────────
#│ editlog.pl for YY-BOARD
#│ YY-BOARD Antispam Version Modified by isso.
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

#-------------------------------------------------
#  記事削除
#-------------------------------------------------
sub dele {
	# POST限定
	if ($postonly && !$post_flag) { &error("不正なアクセスです"); }

	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事Noまたは削除キーが入力モレです"); }

	my ($flg, $pw2, @new);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;
	while (<DAT>) {
		my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw) = split(/<>/);

		if ($in{'no'} == $no) {
			$flg++;
			$pw2 = $pw;
			next;
		} elsif ($in{'no'} == $reno) {
			next;
		}
		push(@new,$_);
	}

	if (!$flg) {
		close(DAT);
		&error("該当の記事が見当たりません");
	}
	if ($pw2 eq "") {
		close(DAT);
		&error("削除キーが設定されていません");
	}
	if (&decrypt($in{'pwd'}, $pw2) != 1) {
		close(DAT);
		&error("削除キーが違います");
	}

	# 更新
	unshift(@new,$top);
	seek(DAT, 0, 0);
	print DAT @new;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 完了メッセージ
	&message("削除が完了しました");
}

#-------------------------------------------------
#  記事修正
#-------------------------------------------------
sub edit {
	if ($in{'no'} eq '' || $in{'pwd'} eq '') {
		&error("記事Noまたは削除キーが入力モレです");
	}

	# 修正実行
	if ($in{'job'} eq "edit" || $in{'kaction'} eq "edit") {

		# フォーム入力チェック
		&formCheck('edit');

		# チェック
		if ($no_wd) { &no_wd; }
		if ($jp_wd) { &jp_wd; }
		if ($urlnum > 0) { &urlnum; }

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

		my $flag = 0;
		if (-e $spamdata) {
			# 禁止URLデータをロード
			open(SPAM,"$spamdata") || &error("Open Error : $spamdata");
			my $SPM = <SPAM>;
			close(SPAM);
			# 禁止URLの書き込みをチェック
			foreach (split(/\,/, $SPM)) {
				if(length($_) > 1) {
					if ($in{'comment'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $in{'name'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $in{'url'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $ngmail && $in{'email'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
					if (!$flag && $ngtitle && $in{'sub'} =~ /\Q$_\E/i) {
						$flag = 1; last; }
				}
			}
		}
		if ($flag) { &error("禁止ワードが含まれています"); }

		my ($flg, $pw2, @new);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		my $top = <DAT>;
		while (<DAT>) {
			chomp;
			my ($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg++;
				$pw2 = $pw;
				$_ = "$no<>$reno<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pw<>$col[$in{'color'}]<>$in{'icon'}<>$tm<>$in{'smail'}<>";
			}
			push(@new,"$_\n");
		}

		if (!$flg) {
			close(DAT);
			&error("該当の記事が見当たりません");
		}
		if ($pw2 eq "") {
			close(DAT);
			&error("削除キーが設定されていません");
		}

		if (&decrypt($in{'pwd'}, $pw2) != 1) {
			close(DAT);
			&error("削除キーが違います");
		}

		# 更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		if($keitai ne 'p') {
			&k_after;
		} else {
			# 完了メッセージ
			&message("修正が完了しました");
		}
	}

	$flag=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sm) = split(/<>/);
		if ($in{'no'} == $no) {
			$pw2 = $pw;
			$flag = 1;
			last;
		}
	}
	close(IN);
	if (!$flag) { &error("該当の記事が見当たりません"); }
	if ($pw2 eq "") { &error("削除キーが設定されていません"); }

	$check = &decrypt($in{'pwd'}, $pw2);
	if ($check != 1) { &error("削除キーが違います"); }

	$com =~ s/<br>/\n/g;
	$pattern = 'https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$pattern" target="_blank">($pattern)<\/a>/$1/go;

	if($keitai ne 'p') {
		&k_form("edit",$no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$in{'pwd'},$col,$ico,$tm,$sm);
	} else {
		if ($ImageView == 1) { &header('ImageUp'); }
		else { &header; }
		print <<EOM;
<form>
<input type=button value="前画面に戻る" onClick="history.back()">
</form>
▽変更する部分のみ修正して送信ボタンを押して下さい。
<p>
<form action="$registcgi" method="$method">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="job" value="edit">
<input type="hidden" name="pwd" value="$in{'pwd'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="reno" value="$in{'reno'}">
<input type="hidden" name="list" value="$in{'list'}">
EOM
		# 管理者
		my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
		if ($adminchk) {
			if ($cnam eq $admin_id && $cpwd eq $pass) {
				$nam = $admin_id;
				if($a_color) { $col = $a_color; }
			}
		}

		# 修正フォーム
		require $formpl;
		&form($nam,$eml,$url,'??',$ico,$col,$sub,$com,$sm);
		print <<EOM;
</form>
</body>
</html>
EOM
	}
	exit;
}



1;
