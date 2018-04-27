#��������������������������������������������������������������������
#�� pastlog.pl for YY-BOARD
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� Modified by isso. 2007
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  �ߋ����O
#-------------------------------------------------
sub past_log {
	open(IN,"$nofile") || &error("Open Error: $nofile");
	my $num = <IN>;
	close(IN);

	$in{'log'} =~ s/\D//g;
	if (!$in{'log'}) { $in{'log'} = $num; }

	&header;
	print <<"EOM";
<form action="$bbscgi">
EOM
	if ($in{'list'} ne "pickup") {
		print qq|<input type="hidden" name="list" value="$in{'list'}">\n|;
	}
	print <<EOM;
<input type="submit" value="&lt; �߂�">
</form>
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="list" value="$in{'list'}">
<table border="0">
<tr><td><b>�ߋ����O</b> <select name="log" class="f">
EOM

	# �ߋ����O�I��
	for ( my $i = $num; $i > 0; --$i ) {
		$i = sprintf("%04d", $i);
		next unless (-e "$pastdir/$i.cgi");

		if ($in{'log'} == $i) {
			print "<option value=\"$i\" selected>$i\n";
		} else {
			print "<option value=\"$i\">$i\n";
		}
	}

	print <<EOM;
</select>
<input type="submit" value="�ړ�"></td></form>
<td width="15"></td><td>
<form action="$bbscgi" method="$method">
<input type="hidden" name="mode" value="past">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="log" value="$in{'log'}">
�L�[���[�h <input type="text" name="word" size="35" value="$in{'word'}" class="f">
���� <select name="cond" class="f">
EOM

	if (!$in{'cond'}) { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}

	print qq|</select> �\\�� <select name="view" class="f">\n|;

	if (!$in{'view'}) { $in{'view'} = 10; }
	foreach (10,15,20,25) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}

	print <<EOM;
</select>
<input type="submit" value="����"></td>
</form>
</tr></table>
EOM

	my $file = sprintf("%s/%04d.cgi", $pastdir,$in{'log'});

	# ��������
	if ($in{'word'} ne "") {

		# ����
		require $searchpl;
		my ($i, $next, $back) = &search($file, $in{'word'}, $in{'view'}, $in{'cond'}, 'past');

		# �y�[�W�J��z��
		my $enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$bbscgi?mode=$mode&log=$in{'log'}&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&list=$in{'list'}\">�O��$in{'view'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$bbscgi?mode=$mode&log=$in{'log'}&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&list=$in{'list'}\">����$in{'view'}��</a>]\n";
		}

		print "</body></html>\n";
		exit;
	}

	print "<dl>\n";

	my $i = 0;
	open(IN,"$file") || &error("Open Error: $file");
	while (<IN>) {
		my ($no,$re,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);

		if ($re eq "") { $i++; }
		if ($i < $page + 1) { next; }
		if ($i > $page + $pastView) { next; }

		$author = $nam;
		require $messagepl;
		if ($eml && $pastmail) { $nam = &emailscript($nam,$no,$eml,$sml,$col,$hos); }

		if ($re) { print "<div style=\"margin-left:22px; margin-top:5px; margin-right:10px;\">\n"; }
		&messageform($no,$re,$dat,$nam,$sub,$com,$url,$pw,$col,$ico,$author,$tm);
		if ($re) { print "</div>\n"; }
	}
	close(IN);

	print <<EOM;
<dt><hr>
</dl>
EOM

	# �y�[�W�ړ��{�^���\��
	if ($page - $pastView >= 0 || $page + $pastView < $i) {
		&mvbtn("$bbscgi?mode=$mode&log=$in{'log'}&page=", $i, $pastView);
	}

	print <<EOM;
</body>
</html>
EOM
	exit;
}



1;

