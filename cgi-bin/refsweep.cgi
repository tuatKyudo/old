#!/usr/local/bin/perl

# Referrer Sweeper v1.1 (Jan-05-2000)
# Copyright (c) 1999-2000 Kan-chan <kan-chan@innocent.com>
#  Web site: http://kan-chan.stbbs.net/download/
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of 
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# Release note:
# v1.1 (Jan-05-2000)
#   Bilingual (English/Japanese) support.
#   Option for delay time.
#   Support for URLs including CGI parameters.
# v1.0 (Aug-12-1999)
#   First release.

# Usage:
# 1. Modify the perl directory written on the top of this script 
#    if it is required.
# 2. Upload files to the CGI directory and change the permission(705).  
#    If you cannot use 705, try 755.
# 3. Call refsweep.cgi 
#    e.g.  refsweep.cgi?url=http://www.yahoo.com/
#      Remove HTTP_REFERER and load http://www.yahoo.com/
#

############################################################
# Settings you may need to modify if necessary             #
# 必要に応じて変更する項目                                 #
############################################################

# Language (JP/EN)
# 言語 (JP/EN)

$language = 'JP';
#$language = 'EN';

# Delay time to load new page
# 新しいページをロードする待ち時間

$delaytime = 0;

############################################################

# Messages
# メッセージ

%MESSAGE = (
'ENpost_method', 'POST method is disabled. Use GET method.', 
'ENurl_not_specified', 'URL is not specified.',
'ENaccessing', 'Accessing...  Wait a moment...',

'JPget_method', 'POSTメソッドでの呼び出しは無効です。GETメソッドを使用してください。',
'JPurl_not_specified', 'URLが指定されていません。',
'JPaccessing', 'アクセス中...  しばらくお待ちください...'
);

############################################################

if ($ENV{'REQUEST_METHOD'} eq "POST"){
	&error('Error', $MESSAGE{$language . 'post_method'});
} else{
	$buffer = $ENV{'QUERY_STRING'};
}
$url = $buffer;
$url =~ s/^url\=(.*)/$1/;
if ($url eq ''){
	&error('Error', $MESSAGE{$language . 'url_not_specified'});
} else{
	print <<"EOF";
Content-type: text/html

<html>
<head>
<title>Referrer-Sweeper</title>
<meta HTTP-EQUIV="refresh" CONTENT="$delaytime; URL=$url">
</head>
<body>
<h1>
$MESSAGE{$language.'accessing'}
<hr>
<center>
<div style="text-align:left;">
<SCRIPT language="JavaScript">
	<!--
	/* efStat from YugenKoubou (http://www.skipup.com/~fuka/) */
	buf = escape(parent.document.referrer);
	ref = "";
	for (i = 0; i < buf.length; i++)
	{
		str = buf.charAt(i);
		ref += (str == "+") ? "%2B" : str;
	}
	scr = screen.width+","+screen.height+","+screen.colorDepth;
	document.write('<a href="http://www.skipup.com/~fuka/"><IMG SRC="./fstat/fcount.cgi?LOG=Sweep&amp;DIGIT=6&amp;REF=',ref,'&amp;SCR=',scr,'" width="1" height="1" border="0" alt="カウンタ"></a>');
	// -->
</SCRIPT>
<NOSCRIPT>
	<a href="http://www.skipup.com/~fuka/"><IMG src="./fstat/fcount.cgi?LOG=Sweep&amp;DIGIT=6&amp;REF=noscript&amp;SCR=-" width="1" height="1" border="0" alt="カウンタ"></a>
</NOSCRIPT>
</div>
$url
</center>
</h1>
</body>
</html>
EOF
}

exit;

sub error{
	if ($language eq 'EN') {
		$exit_msg = 'Click [Back] button on the browser.';
	}
	if ($language eq 'JP') {
		$exit_msg = 'ブラウザの[戻る]ボタンをクリックしてください。';
	}

	print <<"EOF";
Content-type: text/html

<html>
<head>
<title>Error</title>
</head>
$body
<h1>$_[0]</h1>
<h3>$_[1]</h3>
<br>
$exit_msg
</body>
</html>
EOF
	exit;
}
