#┌─────────────────────────────────
#│ message.pl for YY-BOARD
#│ Copyright isso. 2008
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

#-------------------------------------------------
#  email表示
#-------------------------------------------------
sub emailscript {
	my ($na,$no,$em,$sml,$col,$hos) = @_;
	my $name0 = $na;
	if ($nam_col) {
		$name0 = "<font color='$col'>$na</font>&nbsp;&lt;$hos&gt;";
	}
	if ($sml && $webmail) {
		my $nam0 = "<a href=$bbscgi";
		my $nam1 = "?no=$no&mode=writemail&list=$in{'list'}>";
		my $nam2 = "$name0";
		my $nam3 = "</a>";
		$na  = "<span class=\"e\"><script type=\"text/javascript\">\n<!-- //\n";
		$na .= "fcheck(\"$nam2\",\"$nam0\",\"$nam1\",\"$nam3\");\n// -->&nbsp;&lt;$hos&gt;\n</script></span>\n<noscript>";
		$na .= "<a href=\"$bbscgi?mode=noscript\"><span class=\"e\">$name0</span></a>&nbsp;&lt;$hos&gt;</noscript>\n";
	} elsif (!$sml && $em) {
		my ($em0,$em1) = split(/\@/,$em);
		$em0 = &entity($em0);
		$em1 = &entity($em1);
		$na = "<span class=\"e\"><script type=\"text/javascript\">\n<!-- //\n";
		$na .= "address(\"$em0\",\"$name0\",\"$em1\");\n// -->&nbsp;&lt;$hos&gt;\n</script></span>\n";
		$na .= "<noscript><a href=\"$bbscgi?mode=noscript\"><span class=\"e\">$name0</span></a>&nbsp;&lt;$hos&gt;</noscript>\n";
	} else {
		$na = $name0;
	}
	return ($na);
}

#-------------------------------------------------
#  メッセージ表示
#-------------------------------------------------
sub messageform {
	my ($no,$re,$dat,$name,$sub,$com,$url,$pw,$col,$ico,$author,$tm) = @_;
	if ($mode eq "past" || $mode eq "find") {
		$tbl_c = $bgcolor;
	} elsif ($re) {
		$tbl_c = $tbl_col1;
	} else {
		$tbl_c = $tbl_col0;
	}
	if ($thr_bg && $backgif) {
		print qq|<tr><td>\n|;
	} elsif ($in{'list'} eq "new" || !$re) {
		print qq|<tr><td bgcolor="$tblcol">\n|;
	}

	if ($mode eq "past" || $mode eq "find"){
		if ($re) {
			 print qq|<hr noshade size="1" width="95%">\n|;
		 } else {
			print qq|<hr noshade size="1" width="100%">\n|;
		}
	}

	$act = "";
	if ($mode eq "past") {
		$act = "&action=past&log=$in{'log'}";
	}
	if (!$boardmode && $mode eq "all" && $re) {
		print qq|<p><table width="90%" cellpadding="$cellpadding" cellspacing="$cellspacing" border="$border" class="thread">\n|;
		print qq|<tr><td bgcolor="$tblcol">\n|;
	}

	if ($mode ne "past" && $in{'action'} ne "past") {
		print qq|<form action="$bbscgi?#FORM">\n|;
	}
	print qq|<input type="hidden" name="page" value="$page">\n|;
	print qq|<table border="0" cellpadding="0" width="100%" bgcolor="$tbl_c">\n<tr>\n<td>\n|;
	if ($in{'action'} ne "past") {
		if ($mode ne "past" && $mode ne "find") {
			if (!$re) {
				$sub = "$topmark $sub";
			} else {
				$sub = "$comark $sub";
			}
		}
		print qq|<a href="$bbscgi?list=pickup$act&num=$no#$no"><b style="color:$subcol">$sub</b></a> \n|;
	} else {
		 print qq|<b style="color:$subcol">$sub</b> \n|;
	 }

	if ($boardmode) {
		print qq|<a id="$no">投稿者：</a><b>$name</b> \n|;
	} else {
		print qq|<a id="$no">投稿者：</a><b>$name</b> - $dat |;
		print qq|<font color="$subcol">No\.$no</font>|;
	}

	if ($url) {
		print qq| &nbsp; <a href="$url" target="_blank">|;
		print qq|<img src="$imgurl/$home_gif" border=0 align=top alt='HomePage' width="$home_w" height="$home_h">|;
		print qq|</a> &nbsp;\n|;
	}

	if (!$re || $re_box) {
		if ($mode ne "all" && $mode ne "past" && $in{'action'} ne "past") {
			if ($cref eq "on") {
				$checked = "checked";
			} else {
				$checked = "";
			}
			print qq|<input type="hidden" name="mode" value="res">\n|;
			if ($re_box) {
				print qq|&nbsp;<input type="checkbox" name="refmode" value="on" $checked>引用する&nbsp;\n|;
			}
			print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
			print qq|<input type="hidden" name="refnum" value="$no">\n|;
			print qq|<input type="hidden" name="num" value="$no">\n|;
			if ($re) {
				print qq|<input type="submit" name="res_$re" value="返信" class="post">\n|;
			} else {
				print qq|<input type="submit" name="res_$no" value="返信" class="post">\n|;
			}
		}
	}

	# 所定時間以内の投稿は[NEWマーク]表示
	if (time - $tm < $new_time * 3600) {
		print qq| &nbsp; $newmark \n|;
	}
	print qq|</td></form>\n</tr></table>\n|;

	# 引用部色変更
	if ($refcol) {
		$com =~ s/([\>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
	}

	# URL自動リンク
	if ($autolink) {
		$com = &auto_link($com);
	}

	# コメント欄行間
	if (!$lheight) {
		$lheight = "1.2em";
	}

	if ($iconMode) {
		my $alt = "アイコン";
		@ico1 = split(/\s+/, $ico1);
		@ico2 = split(/\s+/, $ico2);
		foreach (0 .. $#ico1) {
			if ($ico1[$_ ] eq "$ico") {
				$alt = $ico2[$_]; last;
			}
		}
		print qq|<table><tr><td><img src="$imgurl/$ico" alt="$alt" title="$alt"></td>\n|;
		print qq|<td><span style="color:$col; line-height: $lheight;">$com</span></td>\n|;
		print qq|</tr></table>\n|;
	} else {
		print qq|<div style="margin-left:22px; margin-top:6px">|;
		print qq|<span style="color:$col; line-height: $lheight;">$com</span></div>\n|;
	}

	if ($boardmode) {
		print qq|<div align="right">\n<span style="color:$subcol">$dat \[ No\.$no \] \n</span></div>\n|;
	}

	# 投稿者編集フォーム
	if ($mode ne "past" && $in{'action'} ne "past") {
		if ($pw) {
			if ($cnam) {
				if ($cnam =~ /\Q$author\E/i || $author =~ /\Q$cnam\E/i) {
					print qq|<form action="$registcgi" method="$method">\n|;
					print qq|<div align="right">\n|;
					print qq|投稿者 <select name="mode">\n|;
					print qq|<option value="edit">修正\n|;
					print qq|<option value="dele">削除</select>\n|;
					print qq|<input type="hidden" name="no" value="$no">\n&nbsp;|;
					print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
					print qq|削除キー <input type="password" name="pwd" size="8" maxlength="8" value="$cpwd">\n|;
					print qq|<input type="submit" value="送信" class="post"></div>\n|;
					print qq|</form>\n|;
				}
			}
		}
	}
}

1;

