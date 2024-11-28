import subprocess
import os
import argparse
import textwrap


def generate_uris(dir_path):
    subprocess.run(f"""
        cd '{dir_path}'
        find . -type f -name "*.png" | while read -r file; do
            filename=$(basename "$file" .png)
            mimetype=$(file -bN --mime-type "$file")
            content=$(base64 -w0 < "$file")
            echo "${{filename}}   url('data:$mimetype;base64,$content')" >> data_uri.txt
        done""", shell=True)

    # Generate the URIs dictionary from the text file
    txt_file_path = os.path.join(dir_path, 'data_uri.txt')
    uri_dict = {}
    with open(txt_file_path, "r") as f:
        for line in f:
            i = line.index("url('data:image/")
            key, value = line[:i].strip(), line[i+5:-3].strip()
            uri_dict[key] = value
    # Delete the generated txt file
    os.remove(txt_file_path)

    return uri_dict


def populate_lichess_css(dir_path, uri_dict):
    # Get the name of the directory, e.g. "Pieces: Merida"
    curr_dir = os.path.basename(dir_path)

    if curr_dir[:6] == "Pieces":
        # Write the CSS file
        with open(f"{dir_path}/Lichess {curr_dir}.css", "w") as f:
            css_content = textwrap.dedent(
                f"""
                /* ==UserStyle==
                @name         Lichess {curr_dir}
                @namespace    USO Archive
                @author       Arthur Huan
                @version      1.0.0
                @preprocessor uso
                ==/UserStyle== */
                @-moz-document domain("lichess.org") {{
                    .is2d .pawn.white {{
                        background-image: url("{uri_dict['w_pawn']}")!important;
                    }}

                    .is2d .pawn.black {{
                        background-image: url("{uri_dict['b_pawn']}")!important;
                    }}

                    .is2d .knight.white {{
                        background-image: url("{uri_dict['w_knight']}")!important;
                    }}

                    .is2d .knight.black {{
                        background-image: url("{uri_dict['b_knight']}")!important;
                    }}

                    .is2d .bishop.white {{
                        background-image: url("{uri_dict['w_bishop']}")!important;
                    }}

                    .is2d .bishop.black {{
                        background-image: url("{uri_dict['b_bishop']}")!important;
                    }}

                    .is2d .rook.white {{
                        background-image: url("{uri_dict['w_rook']}")!important;
                    }}

                    .is2d .rook.black {{
                        background-image: url("{uri_dict['b_rook']}")!important;
                    }}

                    .is2d .queen.white {{
                        background-image: url("{uri_dict['w_queen']}")!important;
                    }}

                    .is2d .queen.black {{
                        background-image: url("{uri_dict['b_queen']}")!important;
                    }}

                    .is2d .king.white {{
                        background-image: url("{uri_dict['w_king']}")!important;
                    }}

                    .is2d .king.black {{
                        background-image: url("{uri_dict['b_king']}")!important;
                    }}
                }}
                """).lstrip()
            f.write(css_content)

    elif curr_dir[:5] == "Board":
        with open(f"{dir_path}/Lichess {curr_dir}.css", "w") as f:
            css_content = textwrap.dedent(
                f"""
                /* ==UserStyle==
                @name         Lichess Board: Green Vinyl
                @namespace    USO Archive
                @author       Arthur Huan
                @description  A board inspired by the green vinyl rollup boards common at tournaments
                @version      1.0.0
                @preprocessor uso
                ==/UserStyle== */
                @-moz-document domain("lichess.org") {{
                    .is2d cg-board::before {{
                        background-image: url("{uri_dict['board']}") !important;
                    }}
                }}
                """).lstrip()
            f.write(css_content)

    else:
        print("The directory cannot be identified as either pieces or board.")
        return


def populate_chesscom_css(dir_path, uri_dict):
    # Get the name of the directory, e.g. "Pieces: Merida"
    curr_dir = os.path.basename(dir_path)

    if curr_dir[:6] == "Pieces":
        # Write the CSS file
        pass

    elif curr_dir[:5] == "Board":
        with open(f"{dir_path}/Chesscom {curr_dir}.css", "w") as f:
            css_content = textwrap.dedent(
                f"""
                /* ==UserStyle==
                @name         Chess.com {curr_dir}
                @namespace    USO Archive
                @author       Arthur Huan
                @version      1.0.0
                @preprocessor uso
                ==/UserStyle== */
                @-moz-document domain("chess.com") {{
                    :root {{
                        --theme-board-style-image: url("{uri_dict['board']}") !important;
                    }}
                    .board {{
                        background-image: var(--theme-board-style-image) !important;
                    }}
                }}
                """).lstrip()
            f.write(css_content)

    else:
        print("The directory cannot be identified as either pieces or board.")
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', type=str, help='Path to the directory containing images')

    target_dir = os.path.abspath(parser.parse_args().dir_path)
    print(f"Target directory: {target_dir}")
    uris = generate_uris(target_dir)
    populate_lichess_css(target_dir, uris)
    populate_chesscom_css(target_dir, uris)
