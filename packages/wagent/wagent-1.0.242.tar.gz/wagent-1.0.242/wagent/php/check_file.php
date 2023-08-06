<?php 
class CheckFile
{
	static function Exists ($fileURL)
	{
		if (filter_var($fileURL, FILTER_VALIDATE_URL) !== false)
			return  CheckFile::UrlExists ($fileURL);
		return file_exists($fileURL);
	}

	static function get_http_response_code($url) 
	{
    	$headers = get_headers($url);
    	return substr($headers [0], 9, 1);
	}

	static function UrlExists ($fileURL)
	{
		$code = CheckFile::get_http_response_code($fileURL);
		return $code != "4" && $code != "5";
	}
}
?>