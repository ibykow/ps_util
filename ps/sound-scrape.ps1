# usage: sound-scrape [youtube video/playlist url/id]

$flags = @(
    "--write-thumbnail", 
    "--write-description"
)

$output_template = '%(artist&{:} - |)s%(title)s [%(id)s].%(ext)s'

$format = "ba[ext=m4a]/ba[ext=mp4]/ba[ext=mp3]/ba/b"

yt-dlp.exe $flags -o $output_template -f $format $args
