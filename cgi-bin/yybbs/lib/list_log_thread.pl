#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� list_log_thread.pl - 2007/09/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �L���X���b�h�\��
#-------------------------------------------------
sub list_log_thread {
	print <<EOM;
<form action="$bbscgi" method="post">
<input type="hidden" name="page" value="$page">
EOM

	foreach (@view) {

		# e-mail�����N
		if ($eml{$_}) { $nam{$_} = "<a href=\"mailto:$eml{$_}\">$nam{$_}</a>"; }

		# �e�L��
		print qq|<p><table width="90%" cellpadding="5" cellspacing="0" border="1" align="center">\n|;
		print qq|<tr><td bgcolor="$tblcol" valign="top">\n|;
		print qq|<b style="color:$subcol">$sub{$_}</b> |;
		print qq|���e�ҁF<b>$nam{$_}</b> ���e���F$dat{$_} |;
		print qq|<span style="color:$subcol">No.$_</span> |;
		if ($url{$_}) {
			print qq|<a href="$url{$_}" target="_blank"><img src="$imgurl/$home_gif" width="$home_w" height="$home_h" alt="home" border="0"></a> |;
		}
		print qq|&nbsp;&nbsp;<input type="submit" name="res:$_" value="�ԐM"><br><br>\n|;

		if ($iconMode) {
			print qq|<table><tr><td><img src="$imgurl/$ico{$_}"></td>\n|;
			print qq|<td><span style="color:$col{$_}">$com{$_}</span></td>\n|;
			print qq|</tr></table>\n|;
		} else {
			print qq|<div style="margin-left:22px; margin-top:6px">|;
			print qq|<span style="color:$col{$_}">$com{$_}</span></div>\n|;
		}

		# ���X�L��
		if (defined($res{$_})) {

			print qq|<div style="margin-left:22px; margin-top:5px;"><hr size="1">\n|;

			foreach my $res ( split(/,/, $res{$_}) ) {

				# e-mail�����N
				if ($eml{$res}) { $nam{$res} = "<a href=\"mailto:$eml{$res}\">$nam{$res}</a>"; }

				print qq|<b style="color:$subcol">$sub{$res}</b> - <b>$nam{$res}</b> |;
				print qq|$dat{$res} <span style="color:$subcol">No.$res</span> |;
				if ($url{$res}) {
					print qq|<a href="$url{$res}" target="_blank"><img src="$imgurl/$home_gif" width="$home_w" height="$home_h" alt="home" border="0"></a>|;
				}
				print "<br>";
				if ($iconMode) {
					print qq|<table><tr><td><img src="$imgurl/$ico{$res}"></td>\n|;
					print qq|<td><span style="color:$col{$res}">$com{$res}</span></td>\n|;
					print qq|</tr></table>\n|;
				} else {
					print qq|<span style="color:$col{$res}">$com{$res}</span><br>\n|;
				}
				print "<br>";
			}
			print "</div>\n";
		}
		print "</td></tr></table></p>\n";
	}
	print "</form>\n";
}


1;

