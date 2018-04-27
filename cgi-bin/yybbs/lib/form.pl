#��������������������������������������������������������������������
#�� form.pl for YY-BOARD
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� Modified by isso. Apr. 2008
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  �V�K���e�t�H�[��
#-------------------------------------------------
sub postform {
	# ���e�L�[
	local($str_plain,$str_crypt);
	if ($regist_key) {
		require $regkeypl;

		($str_plain,$str_crypt) = &pcp_makekey;
	}

	if ($adminchk && $nam eq $a_name) { $nam = $admin_id; }

	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }
	print <<EOM;
<form action="$bbscgi" target="_top">
<input type="hidden" name="list" value="$in{'list'}">
<input type=submit value="&lt; �߂�">
</form>
</div>
EOM

	print qq|<blockquote>\n|;
	print qq|<form method="$method" action="$registcgi">\n|;
	print <<EOM;
<!-- //
<input type="hidden" name="mode" value="write">
// -->
<input type="hidden" name="page" value="$page">
<input type="hidden" name="reno" value="$in{'no'}">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="num" value="$in{'num'}">
<input type="hidden" name="refmode" value="$cref">
EOM

	if ($allowmode) {
		print "<table border=\"$border\" cellspacing=\"0\" class=\"allow\">\n<tr>\n<td>\n",
		"<b> ���e���e�͊Ǘ��҂�������܂ŕ\\������܂���B </b>",
		"</td>\n</tr>\n</table>\n<br>\n";
	}

	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	print "<b>�� �V�K�̃��b�Z�[�W�͉��L�t�H�[�����瓊�e���ĉ�����</b>\n<br>\n";

	&form($cnam,$ceml,$curl,$cpwd,$cico,$ccol,'',$inputform,$csmail,$caikotoba,$cref,'');
	print "</blockquote>\n</form>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  ���e���
#-------------------------------------------------
sub form {
	local($nam,$eml,$url,$pwd,$ico,$col,$sub,$com,$csmail,$caikotoba,$cref,$reply) = @_;
	local(@ico1,@ico2,@col,$ed);

	$pattern = 'https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$pattern" target="_blank">($pattern)<\/a>/$1/go;

	my $access = &encode_bbsmode();
	my $enaddress = &encode_addr();
	if ($keychange && $mode ne "admin" && $mode ne "edit") {
		$url_key  = 'email'; $mail_key = 'url'; $name_key = 'comment'; $comment_key = 'name';
	} else { $url_key  = 'url'; $mail_key = 'email'; $name_key = 'name'; $comment_key = 'comment'; }

	$ed = "���e";
	if ($mode eq "admin" || $mode eq "edit") { $ed = "�C��"; }

	if ($javascriptpost) {
		print <<EOM;
<script type="text/javascript">
<!-- //
fcheck("me='$bbscheckmode' val","<input t","ype='hidden' na","ue='$access'>");
// -->
</script>
EOM
	} else {
		print qq|<input type="hidden" name="$bbscheckmode" value="$access">\n|;
	}

	print <<EOM;
<table border="0" cellspacing="2">
<tr>
  <td nowrap class="form"><a id="FORM"><b>�����O</b></a></td>
  <td nowrap><input type="text" name="$name_key" size="28" value="$nam" class="f"></td>
</tr>
EOM
	if ($aikotoba && $mode ne "admin" && $mode ne "edit") {
		print "<tr>\n  <td nowrap class=\"form\"><b>�������t</b></td>\n  <td>",
		"<input type=\"text\" name=\"aikotoba\" size=\"10\" value=\"$caikotoba\" class=\"f\">",
		"<font color=\"#ff0000\">���K�{</font></td>\n</tr>";
		if ($caikotoba ne $aikotoba) { print "<tr>\n  <td nowrap colspan=\"2\"><b>$hint</b></td>\n</tr>\n"; }
	}
	if ($no_email eq '1') { print qq|<tr class="topdisp">|; $eml = "";} else { print qq|<tr>|; }
	print <<EOM;
  <td nowrap class="form"><b>�d���[��</b></td><td>
    <input type="hidden" name="mail" size="40" value="$enaddress">
    <input type="text" name="$mail_key" size="36" value="$eml" class="f">
EOM
	print "<select name=\"smail\" class=\"f\">\n";
	$selected0 = ""; $selected1 = "";
	if ($csmail eq "1") { $selected1 = "selected=\"selected\"";
	} else { $selected0 = "selected=\"selected\""; }
	print "<option value=\"0\" $selected0>$mailopt\n",
	"<option value=\"1\" $selected1>$usewebmail\n",
	"</select>\n";

	if ($no_email eq '2') { print "���͂���ꍇ�ɂ͕K��<b style=\"color:#FF0000\">����S�p��</b>�����ĉ�����"; }
	print <<EOM;
</td>
</tr>
<tr class="topdisp">
  <td nowrap>Subject</td>
  <td nowrap>
    <input type="text" name="subject" size="36" value="">
    <b style="color:#ff0000">���͋֎~</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>�^�C�g��</b></td>
  <td nowrap>
    <input type="hidden" name="title" size="36" value="" class="f">
    <input type="hidden" name="theme" size="36" value="" class="f">
    <input type="text" name="sub" size="36" value="$sub" class="f">
EOM
	if ($topsort) {
		if ($reply) {
			print qq|<input type="checkbox" name="sage" value="1"> sage\n|;
		}
	}
	print <<EOM;
  </td>
</tr>
  </td>
</tr>
EOM
	if ($boardmode) {
		if ($comment_url) {
		print "<tr>\n  <td colspan=\"2\">\n",
		"�y���b�Z�[�W���̂t�q�k�͐擪�̂��𔲂��ď�������ŉ������B�z\n",
		"  </td></tr>\n\n";
		}
	print <<EOM;
<tr>
  <td colspan="1" class="form">
    <b>���b�Z�[�W
</b></td><td>
EOM
	} else {
	print <<EOM;
<tr>
  <td colspan="2">
    <b>���b�Z�[�W
EOM
		if ($comment_url) {
			print "�y���b�Z�[�W���̂t�q�k�͐擪�̂��𔲂��ď�������ŉ������B�z\n";
		}
		print "</b><br>\n";
	}
	print <<EOM;
    <textarea cols="52" rows="7" name="$comment_key" wrap="soft" class="f">$com</textarea>
  </td>
</tr>
<tr>
  <td colspan="2">
EOM
	my $f_c_d = int(rand(5E07)) + 12E08;
	if ($urlcheck) { print "  ���b�Z�[�W���ɂ�URL���Ɠ���URL���������܂Ȃ��ŉ�����\n"; }
	print <<EOM;
  <input type="hidden" name="$formcheck" value="$f_c_d"></td>
</tr>
<tr class="topdisp">
  <td>URL</td>
  <td><input type="text" name="url2" size="50" value="">
  <b style="color:#ff0000">���͋֎~</b>
  </td>
</tr>
<tr>
  <td nowrap class="form"><b>�t�q�k</b></td>
  <td nowrap><input type="text" size="52" name="$url_key" value="$url" class="f"></td>
</tr>
EOM

	# �Ǘ��҃A�C�R����z��ɕt��
	@ico1 = split(/\s+/, $ico1);
	@ico2 = split(/\s+/, $ico2);
	if ($my_icon) {
		push(@ico1,$my_gif);
		push(@ico2,"�Ǘ��җp");
	}
	if ($iconMode) {
		print "<tr><td nowrap class=\"form\"><b>�C���[�W</b></td><td nowrap>\n",
		"<select name=\"icon\" class=\"f\">\n";
		foreach(0 .. $#ico1) {
			if ($ico eq $ico1[$_]) {
				print "<option value=\"$_\" selected=\"selected\">$ico2[$_]\n";
			} else {
				print "<option value=\"$_\">$ico2[$_]\n";
			}
		}
		print "</select> &nbsp;\n";

		# �C���[�W�Q�Ƃ̃����N
		if ($ImageView == 1) {
			print "[<a href=\"javascript:ImageUp()\">�C���[�W�Q��</a>]";
		} else {
			print "[<a href=\"$bbscgi?mode=image\" target=\"_blank\">�C���[�W�Q��</a>]";
		}
		print "</td></tr>\n";
	}

	if ($pwd ne "??") {
		print "<tr><td nowrap class=\"form\"><b>�폜�L�[</b></td>\n";
		print "<td nowrap><input type=\"password\" name=\"pwd\" size=\"8\" maxlength=\"8\" value=\"$pwd\" class=\"f\">\n";
		print "(�p������8�����ȓ�)</td></tr>\n";

		# ���e�L�[
		if ($regist_key) {
			print qq|<tr><td nowrap class="form"><b>���e�L�[</b></td>\n<td nowrap>|;
			$auto_srt_key = "";
			if ($cnam) { 
				# ���e�L�[4�����o
				if($ENV{'HTTP_REFERER'}) { $srt_key = substr($str_plain,0,4); }
				# ���t�@���[�E�N�b�L�[�L�����ɓ��e�L�[��������
				if($autokey) { $auto_srt_key = $srt_key; }
				print qq|<script type="&#116;&#101;&#120;&#116;/&#x6a;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;">\n<!-- //\n|;
				print qq|fcheck("e='regikey' size='6' style='ime-mode:inactive' valu","<input typ","e='text' nam","e='$auto_srt_key'>");\n|;
				print qq|// -->\n</script>\n|;
				print qq|<noscript>|;
				print qq|<input type="text" name="regikey" size="6" style="ime-mode:inactive" value="xxxxxx">|;
				print qq|</noscript>\n|;
			} else {
				print qq|<input type="text" name="regikey" size="6" style="ime-mode:inactive" value="" class="f">\n|;
			}
			print qq|�i���e�� <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="���e�L�["> ����͂��Ă��������j</td></tr>\n|;
			print qq|<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
		}
	}

	# �F���
	print qq|<tr><td nowrap class="form"><b>�����F</b></td>\n<td nowrap>\n|;
	@col = split(/\s+/, $color);
	if ($col eq "") { $col = 0; }
	$acol = $#col;
	# �Ǘ��ҐF
	if ($adminchk && $nam eq $admin_id) { $acol = $#col+1; $col[$acol] = $a_color; }
	foreach (0 .. $acol) {
		if ($col eq $col[$_] || $col eq $_) {
			print qq|<input type="radio" name="color" value="$_" class="radio" checked="checked">\n|;
			print qq|<font color="$col[$_]">��</font>\n|;
		} else {
			print qq|<input type="radio" name="color" value="$_" class="radio">\n|;
			print qq|<font color="$col[$_]">��</font>\n|;
		}
	}

	print qq|<tr>\n  <td colspan="2">\n|;
	if (!$referercheck || $ENV{'HTTP_REFERER'}) {
		if ($javascriptpost) {
			print qq|<script type="text/javascript">\n<!-- //\n|;
			if ($mode ne "edit" && $mode ne "admin" ) {
				print qq|fcheck("name='mode' value","<input t","ype='hidden' ","='$writevalue'>");\n|;
			}
			print qq|fcheck("value='$ed����' class='post'> <input t","<input t","ype='submit' name='submit' ","ype='reset' value='���Z�b�g' class='post'>");\n|;
			print qq|// -->\n|;
			print qq|</script>\n<noscript><br><b>Javascript��L���ɂ��Ă��������B</b><br><br></noscript>\n|;
		} else {
			if ($mode ne "edit" && $mode ne "admin" ) {
				print qq|    <input type="hidden" name="mode" value="$writevalue">\n|;
			}
			print qq|    <input type="submit" name="submit" value="$ed����" class="post">\n|;
			print qq|    <input type="reset" value="���Z�b�g" class="post">\n|;
		}
	} else {
		print qq|<br>\n<b>�f���֒��ڃA�N�Z�X�����ꍇ�ɂ͓��e�ł��܂���B|;
		print qq|<a href="$homepage">�g�b�v�y�[�W</a>������蒼���Ă��������B</b>\n|;
	}

	print <<EOM;
  </td>
</tr>
</table>
EOM
}



1;

