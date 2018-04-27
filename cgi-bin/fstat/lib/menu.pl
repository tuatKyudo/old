;#+------------------------------------------------------------------------
;#|efStat
;#|初期メニュー
;#+------------------------------------------------------------------------
print <<"_END_";
<FORM action=\"${self}\" method=\"POST\">
<CENTER><TABLE border=\"1\" cellpadding=\"2\" cellspacing=\"0\"><TBODY><TR>
		<TH colspan=\"4\"${tbc[0]}>表\示させる項目</TH>
	</TR><TR>
		<TD${tbc[5]}><INPUT type=\"radio\" name=\"MODE\" value=\"rawlog\" checked>生ログ</TD>
		<TD${tbc[6]}><INPUT type=\"radio\" name=\"MODE\" value=\"count\">カウント数集計</TD>
		<TD${tbc[7]}><INPUT type=\"radio\" name=\"MODE\" value=\"all\">全て表\示</TD>
		<TD${tbc[8]}>　</TD>
	</TR><TR>
		<TD${tbc[5]}><INPUT type=\"radio\" name=\"MODE\" value=\"ref\">参照元統計(系)</TD>
		<TD${tbc[6]}><INPUT type=\"radio\" name=\"MODE\" value=\"host\">ホスト統計(系)</TD>
		<TD${tbc[7]}><INPUT type=\"radio\" name=\"MODE\" value=\"ua\">ブラウザ統計(系)</TD>
		<TD${tbc[8]}><INPUT type=\"radio\" name=\"MODE\" value=\"screen\">画面情報統計(系)</TD>
</TR></TBODY></TABLE></CENTER>
<BR>
<CENTER><TABLE border=\"0\" cellpadding=\"4\" cellspacing=\"0\"><TBODY><TR><TD valign=\"top\">
	<TABLE border=\"1\" cellpadding=\"1\" cellspacing=\"0\"><TBODY><TR>
			<TH colspan=\"3\"${tbc[0]}>表\示リミッタ (半角数字で指定)</TH>
		</TR><TR${tbc[5]}>
			<TH${tbc[1]}>表\示範囲指定</TH>
			<TD colspan=\"2\"><SELECT name=\"d\"><OPTION VALUE=a>全て<OPTION VALUE=t>本日<OPTION VALUE=y>昨日</SELECT></TD>
		</TR><TR${tbc[5]}>
			<TH${tbc[1]}>生ログ</TH>
			<TD>生ログ</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_raw\" value=\"$COOKIE{'LM_raw'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TH rowspan=\"4\"${tbc[2]}>参照元系</TH>
			<TD>参照元</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_ref\" value=\"$COOKIE{'LM_ref'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>TINAMI分析</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_tnm\" value=\"$COOKIE{'LM_tnm'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>Surfers Paradice分析</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_sp\" value=\"$COOKIE{'LM_sp'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>サーチエンジン分析</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_key\" value=\"$COOKIE{'LM_key'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[7]}>
			<TH rowspan=\"2\"${tbc[3]}>ホスト系</TH>
			<TD>ホスト名</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_hst\" value=\"$COOKIE{'LM_hst'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[7]}>
			<TD>国籍別統計</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_dm\" value=\"$COOKIE{'LM_dm'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[8]}>
			<TH${tbc[4]}>ブラウザ系</TH>
			<TD>ブラウザ名</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_ua\" value=\"$COOKIE{'LM_ua'}\" maxlength=\"3\"></TD>
	</TR></TBODY></TABLE>
</TD><TD valign=\"top\" align=\"center\">
	<TABLE border=\"1\" cellpadding=\"1\" cellspacing=\"0\"><TBODY><TR>
			<TH colspan=\"3\"${tbc[0]}>オプション</TH>
		</TR><TR${tbc[5]}>
			<TH align=\"right\"${tbc[1]}>テイストレスモードで表\示</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_tl\" value=\"1\"$check_tl0>させる</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_tl\" value=\"0\"$check_tl1>させない</TD>
		</TR><TR${tbc[6]}>
			<TH align=\"right\"${tbc[2]}>グラフを表\示</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_gr\" value=\"1\"$check_gr0>させる</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_gr\" value=\"0\"$check_gr1>させない</TD>
		</TR><TR${tbc[7]}>
			<TH align=\"right\"${tbc[3]}>参照元へのリンクを許可</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_lk\" value=\"1\"$check_lk0>する</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_lk\" value=\"0\"$check_lk1>しない</TD>
		</TR><TR${tbc[8]}>
			<TH align=\"right\"${tbc[4]}>これら設定情報を保持</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_ck\" value=\"1\"$check_ck0>する</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_ck\" value=\"0\"$check_ck1>しない</TD>
_END_

if ($DoPass) {
print <<"_END_";
			</TR><TR${tbc[8]}>
			<TH align=\"right\"${tbc[4]}>パスワード</TH>
			<TD colspan=\"2\"><INPUT type=\"password\" name=\"PASS\" value=\"$COOKIE{'PASS'}\"size=\"10\" maxlength=\"10\"></TD>
_END_
}

print <<"_END_";
	</TR></TBODY></TABLE>
	<BR><BR>
	<CENTER>
		<INPUT type=\"submit\" value=\"以上の条件でログを表\示\"><BR><BR>
		結果の表\示には時間がかかります。<BR>
		ボタンを押した後<BR>
		しばらくそのままでお待ち下さい。
	</CENTER>
</TD></TR></TBODY></TABLE></CENTER>
</FORM>
_END_

1;
