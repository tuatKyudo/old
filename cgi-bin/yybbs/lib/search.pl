#��������������������������������������������������������������������
#�� search.pl for YY-BOARD
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� Modified by isso. 2007
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  ��������
#-------------------------------------------------
sub search {
	local($file, $word, $view, $cond, $job) = @_;

	# �L�[���[�h��z��
	$word =~ s/\x81\x40/ /g;
	my @wd = split(/\s+/, $word);

	# �t�@�C���W�J
	print "<dl>\n";
	my $i = 0;
	open(IN,"$file") || &error("Open Error: $file");
	my $top = <IN> if ($job ne "past");
	while (<IN>) {
		my $flg;
		foreach my $wd (@wd) {
			if (index($_,$wd) >= 0) {
				$flg++;
				if ($cond eq 'OR') { last; }
			} else {
				if ($cond eq 'AND') { $flg = 0; last; }
			}
		}

		# �q�b�g�����ꍇ
		if ($flg) {
			$i++;
			next if ($i < $page + 1);
			next if ($i > $page + $view);

			($no,$reno,$dat,$nam,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);
			$author = $nam;
			require $messagepl;
			if ($eml && $pastmail) { $nam = &emailscript($nam,$no,$eml,$sml,$col,$hos); }
			&messageform($no,$reno,$dat,$nam,$sub,$com,$url,$pw,$col,$ico,$author,$tm);
		}
	}
	close(IN);

	print <<EOM;
<dt><hr>
�������ʁF<b>$i</b>��
</dl>
EOM

	my $next = $page + $view;
	my $back = $page - $view;
	return ($i, $next, $back);
}



1;

