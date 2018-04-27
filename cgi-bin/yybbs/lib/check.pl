#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ check.pl - 2006/11/14
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<ul>
EOM

	# ログチェック
	my %path = (
		$logfile => "ログファイル",
		$cntfile => "カウントファイル",
		);
	foreach ( keys(%path) ) {
		# パス
		if (-e $_) {
			print "<li>$path{$_}パス : OK\n";

			# パーミッション
			if (-r $_ && -w $_) {
				print "<li>$path{$_}パーミッション : OK\n";
			} else {
				print "<li>$path{$_}パーミッション : NG\n";
			}
		} else {
			print "<li>$path{$_}パス : NG → $_\n";
		}
	}

	# 過去ログ
	print "<li>過去ログ：";
	if ($pastkey == 0) {
		print "設定なし\n";
	} else {
		print "設定あり\n";

		# NOファイル
		if (-e $nofile) {
			print "<li>NOファイルパス：OK\n";
		} else {
			print "<li>NOファイルのパス：NG → $nofile\n";
		}
		if (-r $nofile && -w $nofile) {
			print "<li>NOファイルパーミッション：OK\n";
		} else {
			print "<li>NOファイルパーミッション：NG → $nofile\n";
		}

		# ディレクトリ
		if (-d $pastdir) {
			print "<li>過去ログディレクトリパス：OK\n";
		} else {
			print "<li>過去ログディレクトリのパス：NG → $pastdir\n";
		}
		if (-r $pastdir && -w $pastdir && -x $pastdir) {
			print "<li>過去ログディレクトリパーミッション：OK\n";
		} else {
			print "<li>過去ログディレクトリパーミッション：NG → $pastdir\n";
		}
	}

	print <<EOM;
<li>バージョン : $ver
</ul>
</body>
</html>
EOM
	exit;
}


1;

