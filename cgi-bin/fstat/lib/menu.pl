;#+------------------------------------------------------------------------
;#|efStat
;#|�����˥塼
;#+------------------------------------------------------------------------
print <<"_END_";
<FORM action=\"${self}\" method=\"POST\">
<CENTER><TABLE border=\"1\" cellpadding=\"2\" cellspacing=\"0\"><TBODY><TR>
		<TH colspan=\"4\"${tbc[0]}>ɽ\�����������</TH>
	</TR><TR>
		<TD${tbc[5]}><INPUT type=\"radio\" name=\"MODE\" value=\"rawlog\" checked>����</TD>
		<TD${tbc[6]}><INPUT type=\"radio\" name=\"MODE\" value=\"count\">������ȿ�����</TD>
		<TD${tbc[7]}><INPUT type=\"radio\" name=\"MODE\" value=\"all\">����ɽ\��</TD>
		<TD${tbc[8]}>��</TD>
	</TR><TR>
		<TD${tbc[5]}><INPUT type=\"radio\" name=\"MODE\" value=\"ref\">���ȸ�����(��)</TD>
		<TD${tbc[6]}><INPUT type=\"radio\" name=\"MODE\" value=\"host\">�ۥ�������(��)</TD>
		<TD${tbc[7]}><INPUT type=\"radio\" name=\"MODE\" value=\"ua\">�֥饦������(��)</TD>
		<TD${tbc[8]}><INPUT type=\"radio\" name=\"MODE\" value=\"screen\">���̾�������(��)</TD>
</TR></TBODY></TABLE></CENTER>
<BR>
<CENTER><TABLE border=\"0\" cellpadding=\"4\" cellspacing=\"0\"><TBODY><TR><TD valign=\"top\">
	<TABLE border=\"1\" cellpadding=\"1\" cellspacing=\"0\"><TBODY><TR>
			<TH colspan=\"3\"${tbc[0]}>ɽ\����ߥå� (Ⱦ�ѿ����ǻ���)</TH>
		</TR><TR${tbc[5]}>
			<TH${tbc[1]}>ɽ\���ϰϻ���</TH>
			<TD colspan=\"2\"><SELECT name=\"d\"><OPTION VALUE=a>����<OPTION VALUE=t>����<OPTION VALUE=y>����</SELECT></TD>
		</TR><TR${tbc[5]}>
			<TH${tbc[1]}>����</TH>
			<TD>����</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_raw\" value=\"$COOKIE{'LM_raw'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TH rowspan=\"4\"${tbc[2]}>���ȸ���</TH>
			<TD>���ȸ�</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_ref\" value=\"$COOKIE{'LM_ref'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>TINAMIʬ��</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_tnm\" value=\"$COOKIE{'LM_tnm'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>Surfers Paradiceʬ��</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_sp\" value=\"$COOKIE{'LM_sp'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[6]}>
			<TD>���������󥸥�ʬ��</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_key\" value=\"$COOKIE{'LM_key'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[7]}>
			<TH rowspan=\"2\"${tbc[3]}>�ۥ��ȷ�</TH>
			<TD>�ۥ���̾</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_hst\" value=\"$COOKIE{'LM_hst'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[7]}>
			<TD>����������</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_dm\" value=\"$COOKIE{'LM_dm'}\" maxlength=\"3\"></TD>
		</TR><TR${tbc[8]}>
			<TH${tbc[4]}>�֥饦����</TH>
			<TD>�֥饦��̾</TD>
			<TD><INPUT size=\"3\" type=\"text\" name=\"LM_ua\" value=\"$COOKIE{'LM_ua'}\" maxlength=\"3\"></TD>
	</TR></TBODY></TABLE>
</TD><TD valign=\"top\" align=\"center\">
	<TABLE border=\"1\" cellpadding=\"1\" cellspacing=\"0\"><TBODY><TR>
			<TH colspan=\"3\"${tbc[0]}>���ץ����</TH>
		</TR><TR${tbc[5]}>
			<TH align=\"right\"${tbc[1]}>�ƥ����ȥ쥹�⡼�ɤ�ɽ\��</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_tl\" value=\"1\"$check_tl0>������</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_tl\" value=\"0\"$check_tl1>�����ʤ�</TD>
		</TR><TR${tbc[6]}>
			<TH align=\"right\"${tbc[2]}>����դ�ɽ\��</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_gr\" value=\"1\"$check_gr0>������</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_gr\" value=\"0\"$check_gr1>�����ʤ�</TD>
		</TR><TR${tbc[7]}>
			<TH align=\"right\"${tbc[3]}>���ȸ��ؤΥ�󥯤����</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_lk\" value=\"1\"$check_lk0>����</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_lk\" value=\"0\"$check_lk1>���ʤ�</TD>
		</TR><TR${tbc[8]}>
			<TH align=\"right\"${tbc[4]}>��������������ݻ�</TH>
			<TD><INPUT type=\"radio\" name=\"OPT_ck\" value=\"1\"$check_ck0>����</TD>
			<TD><INPUT type=\"radio\" name=\"OPT_ck\" value=\"0\"$check_ck1>���ʤ�</TD>
_END_

if ($DoPass) {
print <<"_END_";
			</TR><TR${tbc[8]}>
			<TH align=\"right\"${tbc[4]}>�ѥ����</TH>
			<TD colspan=\"2\"><INPUT type=\"password\" name=\"PASS\" value=\"$COOKIE{'PASS'}\"size=\"10\" maxlength=\"10\"></TD>
_END_
}

print <<"_END_";
	</TR></TBODY></TABLE>
	<BR><BR>
	<CENTER>
		<INPUT type=\"submit\" value=\"�ʾ�ξ��ǥ���ɽ\��\"><BR><BR>
		��̤�ɽ\���ˤϻ��֤�������ޤ���<BR>
		�ܥ���򲡤�����<BR>
		���Ф餯���ΤޤޤǤ��Ԥ���������
	</CENTER>
</TD></TR></TBODY></TABLE></CENTER>
</FORM>
_END_

1;
