from .logger import logger

def image(src):
    return f'<img src={src} loading=lazy style="width: 0px; min-width: 100%">'
def video(src):
    return f'<video preload="none" src={src} muted loop controls controlslist="nodownload noremoteplayback noplaybackrate" style="width: 0px; min-width: 100%" class="IV2Z_loopedvideo">'
def short_desc(desc):
    return f'<div id=IV2Z_shortdesc>{desc}</div>'

def format_each(desc, **kwargs):
    if isinstance(desc, dict):
        res = {}
        for k,v in desc.items():
            res[format_each(k, **kwargs)] = format_each(v, **kwargs)
        return res
    if isinstance(desc, list):
        res = []
        for v in desc:
            res.append(format_each(v, **kwargs))
        return res
    return desc.format(**kwargs)
def format_type(desc, lower, lowers=None, upper=None, uppers=None, cap=None):
    """Utility function for nodes with image/latent/mask variants"""
    if lowers is None:
        lowers = lower + 's'
    if cap is None:
        cap = lower.capitalize()
    if upper is None:
        upper = lower.upper()
    if uppers is None:
        uppers = lowers.upper()
    return format_each(desc, lower=lower, lowers=lowers, upper=upper, uppers=uppers, cap=cap)

common_descriptions = {
  'merge_strategy': [
      'Determines what the output resolution will be if input resolutions don\'t match',
      {'match A': 'Always use the resolution for A',
      'match B': 'Always use the resolution for B',
      'match smaller': 'Pick the smaller resolution by area',
      'match larger': 'Pick the larger resolution by area',
      }],
  'scale_method': [
    'Determines what method to use if scaling is required',
 ],
  'crop_method': 'When sizes don\'t match, should the resized image have it\'s aspect ratio changed, or be cropped to maintain aspect ratio',
  'IV2Z_PATH': [
    'This is a IV2Z_PATH input. When edited, it provides a list of possible valid files or directories',
    video('https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite/assets/4284322/729b7185-1fca-41d8-bc8d-a770bb2a5ce6'),
    'The current top-most completion may be selected with Tab',
    'You can navigate up a directory by pressing Ctrl+B (or Ctrl+W if supported by browser)',
    'The filter on suggested file types can be disabled by pressing Ctrl+G.',
    'If converted to an input, this functions as a string',
      ],
    "GetCount": ['Get {cap} Count 🎥🅥🅗🅢', short_desc('Return the number of {lowers} in an input as an INT'),
    {'Inputs': {
        '{lowers}': 'The input {lower}',
        },
     'Outputs': {
         'count': 'The number of {lowers} in the input',
        },
    }],
    "SelectEveryNth": ['Select Every Nth {cap} 🎥🅥🅗🅢', short_desc('Keep only 1 {lower} for every interval'),
    {'Inputs': {
        '{lowers}': 'The input {lower}',
        },
     'Outputs': {
         '{upper}': 'The output {lowers}',
         'count': 'The number of {lowers} in the input',
        },
     'Widgets':{
         'select_every_nth': 'The interval from which one frame is kept. 1 means no frames are skipped.',
         'skip_first_{lowers}': 'A number of frames which that is skipped from the start. This applies before select_every_nth. As a result, multiple copies of the node can each have a different skip_first_frames to divide the {lower} into groups'
        },
    }],
}

descriptions = {
  'IV2Z_VideoCombine': ['Video Combine', short_desc('Combine an image sequence into a video'), {
    'Inputs': {
        'images': 'The images to be turned into a video',
        'audio':'(optional) audio to add to the video',
        'meta_batch': '(optional) Connect to a Meta Batch manager to divide extremely long image sequences into sub batches. See the documentation for Meta Batch Manager',
        'vae':['(optional) If provided, the node will take latents as input instead of images. This drastically reduces the required RAM (not VRAM) when working with long (100+ frames) sequences',
               "Unlike on Load Video, this isn't always a strict upgrade over using a standalone VAE Decode.",
               "If you have multiple Video Combine outputs, then the VAE decode will be performed for each output node increasing execution time",
               "If you make any change to output settings on the Video Combine (such as changing the output format), the VAE decode will be performed again as the decoded result is (by design) not cached",
               ]
        },
    'Widgets':{
        'frame_rate': 'The frame rate which will be used for the output video. Consider converting this to an input and connecting this to a Load Video with Video Info(Loaded)->fps. When including audio, failure to properly set this will result in audio desync',
        'loop_count': 'The number of additional times the video should repeat. Can cause performance issues when used with long (100+ frames) sequences',
        'filename_prefix': 'A prefix to add to the name of the output filename. This can include subfolders or format strings.',
        'format': 'The output format to use. Formats starting with, \'image\' are saved with PIL, but formats starting with \'video\' utilize the video_formats system. \'video\' options require ffmpeg and selecting one frequently adds additional options to the node.',
        'pingpong': 'Play the video normally, then repeat the video in reverse so that it \'pingpongs\' back and forth. This is frequently used to minimize the appearance of skips on very short animations.',
        'save_output': 'Specifies if output files should be saved to the output folder, or the temporary output folder',
         'videopreview': 'Displays a preview for the processed result. If advanced previews is enabled, the output is always converted to a format viewable from the browser. If the video has audio, it will also be previewed when moused over. Additional preview options can be accessed with right click.',
        },
    'Common Format Widgets': {
        'crf': 'Determines how much to prioritize quality over filesize. Numbers vary between formats, but on each format that includes it, the default value provides visually loss less output',
        'pix_fmt': ['The pixel format to use for output. Alternative options will often have higher quality at the cost of increased file size and reduced compatibility with external software.', {
            'yuv420p': 'The most common and default format',
            'yuv420p10le': 'Use 10 bit color depth. This can improve color quality when combined with 16bit input color depth',
            'yuva420p': 'Include transparency in the output video'
            }],
        'input_color_depth': 'IV2Z supports outputting 16bit images. While this produces higher quality output, the difference usually isn\'t visible without postprocessing and it significantly increases file size and processing time.',
        'save_metadata': 'Determines if metadata for the workflow should be included in the output video file',
        }
    }],
}

def as_html(entry, depth=0):
    if isinstance(entry, dict):
        size = 0.8 if depth < 2 else 1
        html = ''
        for k in entry:
            if k == "collapsed":
                continue
            collapse_single = k.endswith("_collapsed")
            if collapse_single:
                name = k[:-len("_collapsed")]
            else:
                name = k
            collapse_flag = ' IV2Z_precollapse' if entry.get("collapsed", False) or collapse_single else ''
            html += f'<div IV2Z_title=\"{name}\" style=\"display: flex; font-size: {size}em\" class=\"IV2Z_collapse{collapse_flag}\"><div style=\"color: #AAA; height: 1.5em;\">[<span style=\"font-family: monospace\">-</span>]</div><div style=\"width: 100%\">{name}: {as_html(entry[k], depth=depth+1)}</div></div>'
        return html
    if isinstance(entry, list):
        if depth == 0:
            depth += 1
            size = .8
        else:
            size = 1
        html = ''
        html += entry[0]
        for i in entry[1:]:
            html += f'<div style=\"font-size: {size}em\">{as_html(i, depth=depth)}</div>'
        return html
    return str(entry)

def format_descriptions(nodes):
    for k in descriptions:
        if k.endswith("_collapsed"):
            k = k[:-len("_collapsed")]
        nodes[k].DESCRIPTION = as_html(descriptions[k])
    undocumented_nodes = []
    for k in nodes:
        if not hasattr(nodes[k], "DESCRIPTION"):
            undocumented_nodes.append(k)
    if len(undocumented_nodes) > 0:
        logger.warning('Some nodes have not been documented %s', undocumented_nodes)

