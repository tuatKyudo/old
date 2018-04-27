#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ list_log_tree.pl - 2007/09/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  ツリー表示
#-------------------------------------------------
sub list_log_tree {
	print <<EOM;
<blockquote>
<form action="$bbscgi" method="post">
<input type="hidden" name="page" value="$page">
EOM

	foreach (@view) {

		# 親記事
		print qq|<a href="$readcgi?mode=all&list=tree&no=$_" title="ツリーを一括表\示">▼</a> |;
		print qq|<a href="$readcgi?list=tree&no=$_">$sub{$_}</a> - <b>$nam{$_}</b> $dat{$_} <span style="color:$subcol">No.$_</span><br>\n|;

		# レス記事
		if (defined($res{$_})) {
			my $max = @res = split(/,/, $res{$_});
			my $i = 0;
			foreach my $res (@res) {
				$i++;
				my $tree;
				if ($i == $max) { $tree = "└"; } else { $tree = "├"; }

				print "&nbsp" x 5;
				print qq|$tree <a href="$readcgi?list=tree&no=$res&top=$_">$sub{$res}</a> - <b>$nam{$res}</b> $dat{$res} <span style="color:$subcol">No.$res</span><br>\n|;

			}
		}

		print "<br>\n";
	}

	print <<EOM;
</form>
</blockquote>
EOM
}


1;

