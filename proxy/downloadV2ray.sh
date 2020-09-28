# You can modify it to /usr/local/lib/v2ray/
DAT_PATH='/usr/bin/v2ray/'
# You can modify it to /etc/v2ray/
JSON_PATH='/usr/local/etc/v2ray/'

# $(uname -m)
# k3
MACHINE='arm32-v5'

identify_the_operating_system_and_architecture() {
    if [[ "$(uname)" == 'Linux' ]]; then
        case "$(uname -m)" in
            'i386' | 'i686')
                MACHINE='32'
                ;;
            'amd64' | 'x86_64')
                MACHINE='64'
                ;;
            'armv5tel')
                MACHINE='arm32-v5'
                ;;
            'armv6l')
                MACHINE='arm32-v6'
                ;;
            'armv7' | 'armv7l' )
                MACHINE='arm32-v7a'
                ;;
            'armv8' | 'aarch64')
                MACHINE='arm64-v8a'
                ;;
            'mips')	
                MACHINE='mips32'
                ;;
            'mipsle')
                MACHINE='mips32le'
                ;;
            'mips64')
                MACHINE='mips64'
                ;;
            'mips64le')
                MACHINE='mips64le'
                ;;
            'ppc64')
                MACHINE='ppc64'
                ;;
            'ppc64le')
                MACHINE='ppc64le'
                ;;
            'riscv64')
                MACHINE='riscv64'
                ;;
            's390x')
                MACHINE='s390x'
                ;;
            *)
                echo "error: The architecture is not supported."
                exit 1
                ;;
        esac
        if [[ ! -f '/etc/os-release' ]]; then
            echo "error: Don't use outdated Linux distributions."
            exit 1
        fi
 
    else
        echo "error: This operating system is not supported."
        exit 1
    fi
}

version_number() {
    case "$1" in
        'v'*)
            echo "$1"
            ;;
        *)
            echo "v$1"
            ;;
    esac
}

get_version() {
    # 0: Install or update V2Ray.
    # 1: Installed or no new version of V2Ray.
    # 2: Install the specified version of V2Ray.
    if [[ -z "$VERSION" ]]; then
 
        # Get V2Ray release version number
        TMP_FILE="$(mktemp)"
        echo 临时文件：$TMP_FILE
        # DO NOT QUOTE THESE `${PROXY}` VARIABLES!
        if ! "curl" ${PROXY} -o "$TMP_FILE" 'https://api.github.com/repos/v2fly/v2ray-core/releases/latest'; then
            "rm" "$TMP_FILE"
            echo 'error: Failed to get release list, please check your network.'
            exit 1
        fi
        RELEASE_LATEST="$(sed 'y/,/\n/' "$TMP_FILE" | grep 'tag_name' | awk -F '"' '{print $4}')"
        "rm" "$TMP_FILE"
        RELEASE_VERSION="$(version_number "$RELEASE_LATEST")"
        # Compare V2Ray version numbers
        if [[ "$RELEASE_VERSION" != "$CURRENT_VERSION" ]]; then
            RELEASE_VERSIONSION_NUMBER="${RELEASE_VERSION#v}"
            RELEASE_MAJOR_VERSION_NUMBER="${RELEASE_VERSIONSION_NUMBER%%.*}"
            RELEASE_MINOR_VERSION_NUMBER="$(echo "$RELEASE_VERSIONSION_NUMBER" | awk -F '.' '{print $2}')"
            RELEASE_MINIMUM_VERSION_NUMBER="${RELEASE_VERSIONSION_NUMBER##*.}"
            CURRENT_VERSIONSION_NUMBER="$(echo "${CURRENT_VERSION#v}" | sed 's/-.*//')"
            CURRENT_MAJOR_VERSION_NUMBER="${CURRENT_VERSIONSION_NUMBER%%.*}"
            CURRENT_MINOR_VERSION_NUMBER="$(echo "$CURRENT_VERSIONSION_NUMBER" | awk -F '.' '{print $2}')"
            CURRENT_MINIMUM_VERSION_NUMBER="${CURRENT_VERSIONSION_NUMBER##*.}"
            if [[ "$RELEASE_MAJOR_VERSION_NUMBER" -gt "$CURRENT_MAJOR_VERSION_NUMBER" ]]; then
                return 0
            elif [[ "$RELEASE_MAJOR_VERSION_NUMBER" -eq "$CURRENT_MAJOR_VERSION_NUMBER" ]]; then
                if [[ "$RELEASE_MINOR_VERSION_NUMBER" -gt "$CURRENT_MINOR_VERSION_NUMBER" ]]; then
                    return 0
                elif [[ "$RELEASE_MINOR_VERSION_NUMBER" -eq "$CURRENT_MINOR_VERSION_NUMBER" ]]; then
                    if [[ "$RELEASE_MINIMUM_VERSION_NUMBER" -gt "$CURRENT_MINIMUM_VERSION_NUMBER" ]]; then
                        return 0
                    else
                        return 1
                    fi
                else
                    return 1
                fi
            else
                return 1
            fi
        elif [[ "$RELEASE_VERSION" == "$CURRENT_VERSION" ]]; then
            return 1
        fi
    else
        RELEASE_VERSION="$(version_number "$VERSION")"
        return 2
    fi
}

decompression() {
    if ! unzip -q "$1" -d "$TMP_DIRECTORY"; then
        echo 'error: V2Ray decompression failed.'
        "rm" -r "$TMP_DIRECTORY"
        echo "removed: $TMP_DIRECTORY"
        exit 1
    fi
    echo "info: Extract the V2Ray package to $TMP_DIRECTORY and prepare it for installation."
}


download_v2ray() {
    "mkdir" -p "$TMP_DIRECTORY"
    DOWNLOAD_LINK="https://github.com/v2fly/v2ray-core/releases/download/$RELEASE_VERSION/v2ray-linux-$MACHINE.zip"
    echo "Downloading V2Ray archive: $DOWNLOAD_LINK"
    if ! "curl" ${PROXY} -L -H 'Cache-Control: no-cache' -o "$ZIP_FILE" "$DOWNLOAD_LINK"; then
        echo 'error: Download failed! Please check your network or try again.'
        return 1
    fi
    echo "Downloading verification file for V2Ray archive: $DOWNLOAD_LINK.dgst"
    if ! "curl" ${PROXY} -L -H 'Cache-Control: no-cache' -o "$ZIP_FILE.dgst" "$DOWNLOAD_LINK.dgst"; then
        echo 'error: Download failed! Please check your network or try again.'
        return 1
    fi
    if [[ "$(cat "$ZIP_FILE".dgst)" == 'Not Found' ]]; then
        echo 'error: This version does not support verification. Please replace with another version.'
        return 1
    fi

    # Verification of V2Ray archive
    for LISTSUM in 'md5' 'sha1' 'sha256' 'sha512'; do
        SUM="$(${LISTSUM}sum "$ZIP_FILE" | sed 's/ .*//')"
        CHECKSUM="$(grep ${LISTSUM^^} "$ZIP_FILE".dgst | grep "$SUM" -o -a | uniq)"
        if [[ "$SUM" != "$CHECKSUM" ]]; then
            echo 'error: Check failed! Please check your network or try again.'
            return 1
        fi
    done
}



decompression() {
    if ! unzip -q "$1" -d "$TMP_DIRECTORY"; then
        echo 'error: V2Ray decompression failed.'
        "rm" -r "$TMP_DIRECTORY"
        echo "removed: $TMP_DIRECTORY"
        exit 1
    fi
    echo "info: Extract the V2Ray package to $TMP_DIRECTORY and prepare it for installation."
}

install_file() {
    NAME="$1"
    if [[ "$NAME" == 'v2ray' ]] || [[ "$NAME" == 'v2ctl' ]]; then
        install -m 755 "${TMP_DIRECTORY}/$NAME" "/usr/local/bin/$NAME"
    elif [[ "$NAME" == 'geoip.dat' ]] || [[ "$NAME" == 'geosite.dat' ]]; then

        install -m 644 "${TMP_DIRECTORY}/$NAME" "${DAT_PATH}$NAME"
    fi
}

main() {


    # Two very important variables
    TMP_DIRECTORY="$(mktemp -du)"
    ZIP_FILE="${TMP_DIRECTORY}/v2ray-linux-$MACHINE.zip"

	
	get_version
	NUMBER="$?"
	if [[ "$NUMBER" -eq '0' ]] || [[ "$FORCE" -eq '1' ]] || [[ "$NUMBER" -eq 2 ]]; then
	    echo "info: Installing V2Ray $RELEASE_VERSION for $(uname -m)"
	    download_v2ray
	    if [[ "$?" -eq '1' ]]; then
	        "rm" -r "$TMP_DIRECTORY"
	        echo "removed: $TMP_DIRECTORY"
	        exit 0
	    fi
	    decompression "$ZIP_FILE"
	    upx -vf --best -k $TMP_DIRECTORY/v2ray $$TMP_DIRECTORY/v2ctl
	elif [[ "$NUMBER" -eq '1' ]]; then
	    echo "info: No new version. The current version of V2Ray is $CURRENT_VERSION ."
	    exit 0
  fi
}

main

:'
# run on router
cd /tmp/upload
chmod a+x v2ray v2ctl
mv v2ray /usr/bin/v2ray/v2ray
mv v2ctl /usr/bin/v2ray/v2ctl

mkdir /usr/local
mkdir /usr/local/etcl
mkdir /usr/local/etc/v2ray
mv config.json /usr/local/etc/v2ray
mv 00_log.json /usr/local/etc/v2ray
mkdir -p /usr/local/share/v2ray
mv geo* /usr/bin/v2ray/
nohup /usr/bin/v2ray/v2ray -c /usr/local/etc/v2ray/config.json -c /usr/local/etc/v2ray/00_log.json > /tmp/nohup.log 2>&1 &
'
