#��������������������������������������������������������������������
#�� newsort.pl for YY-BOARD
#�� Copyright isso. May, 2007
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  �V�����\��
#-------------------------------------------------
sub newsort {
	# �L���X���b�h����
	$i = 0;
	$flag = 0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		chomp;
		($no,$re,$dat,$name,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);
		$no{$i}   = $no;
		$re{$i}   = $re;
		$dat{$i}  = $dat;
		$name{$i} = $name;
		$eml{$i}  = $eml;
		$sub{$i}  = $sub;
		$com{$i}  = $com;
		$url{$i}  = $url;
		$hos{$i}  = $hos;
		$pw{$i}   = $pw;
		$col{$i}  = $col;
		$ico{$i}  = $ico;
		$tm{$i}   = $tm;
		$sml{$i}  = $sml;
		$i++;
	}
	close(IN);

	# �\�[�g����
	$j = 0;
	$x = 0;
	foreach (sort { ($no{$b} <=> $no{$a}) } keys(%no)) {
		$j++;
		if ($j < $in{'page'} + 1) { next; }
		if ($j > $in{'page'} + $npage) { next; }

		# �薼�̒���
		if (length($sub{$_}) > $sub_len*2) {
			$sub{$_} = substr($sub{$_},0,$sub_len*2);
			$sub{$_} .= "...";
		}

		$author{$_} = $name{$_};
		require $messagepl;
		$name{$_} = &emailscript($name{$_},$no{$_},$eml{$_},$sml{$_},$col{$_},$hos{$_});

		print "<table width=\"90%\" cellpadding=\"$cellpadding\" cellspacing=\"$cellspacing\" border=\"$border\" class=\"thread\">\n";

		&messageform($no{$_},$re{$_},$dat{$_},$name{$_},$sub{$_},
		$com{$_},$url{$_},$pw{$_},$col{$_},$ico{$_},$author{$_},$tm{$_});

		print "</TD></TR></TABLE><br></center>\n";
	}

	$next = $in{'page'} + $npage;
	$back = $in{'page'} - $npage;

	print "<div align=\"left\"><blockquote><table border=\"0\"><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$bbscgi\" method=\"$method\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$back\">\n";
		print "<input type=\"hidden\" name=\"list\" value=\"new\">\n";
		print "<input type=\"submit\" value=\"�O���\"></form></td>\n";
	}
	if ($next < $j) {
		print "<td><form action=\"$bbscgi\" method=\"$method\">\n";
		print "<input type=\"hidden\" name=\"page\" value=\"$next\">\n";
		print "<input type=\"hidden\" name=\"list\" value=\"new\">\n";
		print "<input type=\"submit\" value=\"�����\"></form></td>\n";
	}

	print "</tr>\n</table></blockquote>\n</div>\n";
}


1;

