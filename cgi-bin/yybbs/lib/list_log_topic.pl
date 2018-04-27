#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ list_log_topic.pl - 2007/09/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  トピック表示
#-------------------------------------------------
sub list_log_topic {
	print <<EOM;
<p>
<table border="1" align="center" cellpadding="3" cellspacing="0" width="90%">
<tr>
  <th nowrap bgcolor="$tblcol">No.</th>
  <th nowrap bgcolor="$tblcol">件名</th>
  <th nowrap bgcolor="$tblcol">作成者</th>
  <th nowrap bgcolor="$tblcol">返信</th>
  <th nowrap bgcolor="$tblcol">最終更新</th>
</tr>
EOM

	foreach (@view) {

		# レス数
		my $res = @res = split(/,/, $res{$_});

		# 最終投稿者
		my $last;
		if ($res) {
			$last_name = $nam{$res[-1]};
			$last_date = $dat{$res[-1]};
		} else {
			$last_name = $nam{$_};
			$last_date = $dat{$_};
		}

		# 親記事
		print qq|<tr><td align="center" bgcolor="$tblcol">$_</td>|;
		print qq|<td width="90%" bgcolor="$tblcol"><a href="$readcgi?mode=all&list=topic&no=$_">$sub{$_}</a></td>|;
		print qq|<td nowrap bgcolor="$tblcol"><b>$nam{$_}</b></td>|;
		print qq|<td align="center" bgcolor="$tblcol">$res</td>|;
		print qq|<td nowrap bgcolor="$tblcol"><font size="-1">$last_date<br>by $last_name</font></td></tr>\n|;
	}

	print <<EOM;
</table>
EOM
}


1;

