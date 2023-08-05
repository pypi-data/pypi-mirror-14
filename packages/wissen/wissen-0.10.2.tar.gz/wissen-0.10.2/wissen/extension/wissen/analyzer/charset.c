
int ischar (char ch) {
	return (isalnum (ch) || ch >= 132);
}

int isunicode (char a, char b) {
	return ((172 <= a <= 215) && (0 <= b <= 255));
}

int iseuckr (char a, char b) {
	return ((161 <= a <= 254) && (161 <= b <= 254));
}

int isksc5601 (char a, char b) {
	return ((132 <= a <= 211) && (65 <= b <= 126 || 129 <= b <= 254));
}
