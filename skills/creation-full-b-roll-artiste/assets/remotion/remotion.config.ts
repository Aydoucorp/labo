// Configuration Remotion par defaut. Les options de rendu (codec, crf, navigateur)
// sont passees en ligne de commande par scripts/render.py.
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
