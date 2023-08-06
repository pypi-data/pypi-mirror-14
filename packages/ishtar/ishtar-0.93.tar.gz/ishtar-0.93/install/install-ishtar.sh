#!/bin/sh

set -e

command_exists() {
    command -v "$@" > /dev/null 2>&1
}

# Check if this is a forked Linux distro
check_forked() {
    # Check for lsb_release command existence, it usually exists in forked distros
    if command_exists lsb_release; then
        # Check if the `-u` option is supported
        set +e
        lsb_release -a -u > /dev/null 2>&1
        lsb_release_exit_code=$?
        set -e

        # Check if the command has exited successfully, it means we're in a forked distro
        if [ "$lsb_release_exit_code" = "0" ]; then
            # Print info about current distro
            cat <<-EOF
            You're using '$lsb_dist' version '$dist_version'.
EOF

            # Get the upstream release info
            lsb_dist=$(lsb_release -a -u 2>&1 | tr '[:upper:]' '[:lower:]' | grep -E 'id' | cut -d ':' -f 2 | tr -d '[[:space:]]')
            dist_version=$(lsb_release -a -u 2>&1 | tr '[:upper:]' '[:lower:]' | grep -E 'codename' | cut -d ':' -f 2 | tr -d '[[:space:]]')

            # Print info about upstream distro
            cat <<-EOF
            Upstream release is '$lsb_dist' version '$dist_version'.
EOF
        fi
    fi
}

do_install() {

    cat >&2 <<-'EOF'

*******************************************************************************
++++++                    Ishtar installation script                     ++++++
*******************************************************************************

EOF

    # check user
    user="$(id -un 2>/dev/null || true)"

    sh_c='sh -c'
    if [ "$user" != 'root' ]; then
        if command_exists sudo; then
            sh_c='sudo -E sh -c'
        elif command_exists su; then
            sh_c='su -c'
        else
            cat >&2 <<-'EOF'
  Error: this installer needs the ability to run commands as root.
  We are unable to find either "sudo" or "su" available to make this happen.
EOF
            exit 1
        fi
    fi

    # check distribution
    lsb_dist=''
    dist_version=''
    if command_exists lsb_release; then
        lsb_dist="$(lsb_release -si)"
    fi
    if [ -z "$lsb_dist" ] && [ -r /etc/lsb-release ]; then
        lsb_dist="$(. /etc/lsb-release && echo "$DISTRIB_ID")"
    fi
    if [ -z "$lsb_dist" ] && [ -r /etc/debian_version ]; then
        lsb_dist='debian'
    fi
    if [ -z "$lsb_dist" ] && [ -r /etc/fedora-release ]; then
        lsb_dist='fedora'
    fi
    if [ -z "$lsb_dist" ] && [ -r /etc/oracle-release ]; then
        lsb_dist='oracleserver'
    fi
    if [ -z "$lsb_dist" ]; then
        if [ -r /etc/centos-release ] || [ -r /etc/redhat-release ]; then
            lsb_dist='centos'
        fi
    fi
    if [ -z "$lsb_dist" ] && [ -r /etc/os-release ]; then
        lsb_dist="$(. /etc/os-release && echo "$ID")"
    fi

    lsb_dist="$(echo "$lsb_dist" | tr '[:upper:]' '[:lower:]')"

    case "$lsb_dist" in

        ubuntu)
            if command_exists lsb_release; then
                dist_version="$(lsb_release --codename | cut -f2)"
            fi
            if [ -z "$dist_version" ] && [ -r /etc/lsb-release ]; then
                dist_version="$(. /etc/lsb-release && echo "$DISTRIB_CODENAME")"
            fi
        ;;

        debian)
            dist_version="$(cat /etc/debian_version | sed 's/\/.*//' | sed 's/\..*//')"
            case "$dist_version" in
                8)
                    dist_version="jessie"
                ;;
                7)
                    dist_version="wheezy"
                ;;
            esac
        ;;

        oracleserver)
            # need to switch lsb_dist to match yum repo URL
            lsb_dist="oraclelinux"
            dist_version="$(rpm -q --whatprovides redhat-release --queryformat "%{VERSION}\n" | sed 's/\/.*//' | sed 's/\..*//' | sed 's/Server*//')"
        ;;

        fedora|centos)
            dist_version="$(rpm -q --whatprovides redhat-release --queryformat "%{VERSION}\n" | sed 's/\/.*//' | sed 's/\..*//' | sed 's/Server*//')"
        ;;

        *)
            if command_exists lsb_release; then
                dist_version="$(lsb_release --codename | cut -f2)"
            fi
            if [ -z "$dist_version" ] && [ -r /etc/os-release ]; then
                dist_version="$(. /etc/os-release && echo "$VERSION_ID")"
            fi
        ;;


    esac

    # Check if this is a forked Linux distro
    check_forked

    case "$lsb_dist" in
        ubuntu|debian)
            ;;
        *)
            cat >&2 <<-'EOF'

  Sorry. Either your platform is not easily detectable or not supported by
  this installer.

EOF
            exit 1
    esac

    default_db=''
    cat >&2 <<-'EOF'

-------------------------------------------------------------------------------
  A PostgreSQL database is needed to install Ishtar. If you do not plan to use
  a database host on another computer you need to install PostgreSQL.

EOF
    while [ "$default_db" == '' ]
    do
        read -p '* Default PostgreSQL host? [localhost] ' choice
        if [ "$choice" == '' ]; then
            default_db='127.0.0.1'
        elif [ "$choice" == 'localhost' ]; then
            default_db='127.0.0.1'
        else
            default_db=$choice
        fi
    done

    webserver=''
    cat >&2 <<-'EOF'

-------------------------------------------------------------------------------
  A webserver is needed to make Ishtar available to the outside.
  Be carreful if another webserver is already configured, you'll have to serve
  your pages on a different port.

EOF
    MSG=""
    while [ "$webserver" == '' ]
    do
        read -p '* Which webserver do you want to use? ([nginx]/none) ' choice
        case "$choice" in
            nginx ) webserver="nginx";;
            none ) webserver="none";;
            '' ) webserver="nginx";;
        esac
    done

    version=''
    cat >&2 <<-'EOF'

-------------------------------------------------------------------------------
  Two version are usually available for Ishtar: master/stable. Master is the
  bleeding edge version and you can experience problems with this version.
  Stable is the safest choice.

EOF
    while [ "$version" == '' ]
    do
        read -p "* Which version would you like to use? ([stable]/master) " choice
        case "$choice" in
            stable ) version="stable";;
            master ) version="master";;
            '' ) version="stable";;
        esac
    done

    etc_path="/etc/ishtar/"$version"/"
    if [ -d "$etc_path" ]; then
        echo ""
        echo "ERROR: it seems that "$etc_path" already exists. If this is a remnant "
        echo "of an old installation please delete this path before installing."
        exit 1
    fi


    install_path=''
    cat >&2 <<-'EOF'

-------------------------------------------------------------------------------
  By default Ishtar base path is '/srv/'. With this base path Ishtar is
  installed in '/srv/ishtar/choosen_version/'.

EOF
    while [ "$install_path" == '' ]
    do
        read -p "* Which base install path for Ishtar? [/srv/] " choice
        if [ -z "$choice" ]; then
            install_path='/srv/'
        elif [ ! -d "$choice" ]; then
            echo 'Not a valid path.'
        else
            install_path=$choice
        fi
    done

    full_install_path=$install_path'/ishtar/'$version
    if [ -d "$full_install_path" ]; then
        echo ""
        echo "ERROR: it seems that "$full_install_path" already exists. If this is a "
        echo "remnant of an old installation please delete this directory before installing."
        exit 1
    fi

    echo ""
    echo "*******************************************************************************"
    echo ""

    # Run setup for each distro accordingly
    case "$lsb_dist" in
        ubuntu|debian)
            if [ "$dist_version" != "wheezy" ]; then
                cat >&2 <<-'EOF'

  Sorry this script cannot manage your version of Debian/Ubuntu.

EOF
                exit 1
            fi

            export DEBIAN_FRONTEND=noninteractive
            ( set -x; $sh_c 'sleep 3; apt-get update' )
            if [ "$default_db" == 'localhost' ]; then
                POSTGIS=postgresql-9.1-postgis
                if [ "$dist_version" == "jessie" ]; then
                    POSTGIS=postgresql-9.4-postgis-2.1
                fi
                ( set -x; $sh_c 'sleep 3; apt-get install -y -q postgresql '$POSTGIS )
            fi
            if ! command_exists git; then
                echo "-------------------------------------------------------------------------------";
                echo "Installing git...";
                echo "";
                ( set -x; $sh_c 'sleep 3; apt-get install -y -q git' )
            fi
            if ! command_exists apg; then
                echo "-------------------------------------------------------------------------------";
                echo "Installing apg...";
                echo "";
                ( set -x; $sh_c 'sleep 3; apt-get install -y -q apg' )
            fi
            if ! command_exists pip; then
                echo "-------------------------------------------------------------------------------";
                echo "Installing pip...";
                echo "";
                ( set -x; $sh_c 'sleep 3; apt-get install -y -q python-pip' )
            fi
            if [ "$webserver" == 'nginx' ]; then
                echo "-------------------------------------------------------------------------------";
                echo "Installing nginx and uwsgi...";
                echo "";
                ( set -x; $sh_c 'sleep 3; apt-get install -y -q  uwsgi uwsgi-plugin-python nginx' )
            fi

            echo "-------------------------------------------------------------------------------";
            echo "Installing Ishtar dependencies"
            echo "";
            ( set -x; $sh_c 'sleep 3; apt-get install -y -q python python-django \
      libjs-jquery libjs-jquery-ui python-pisa python-django-registration \
      python-utidylib python-lxml python-imaging python-django-south \
      python-psycopg2 python-gdal gettext python-unicodecsv memcached \
      python-tidylib python-django-extra-views python-memcache python-dbf' )
            ;;

    esac
    echo "-------------------------------------------------------------------------------";
    echo "Installing BeautifulSoup4"
    echo "";

    ( set -x; $sh_c 'pip install BeautifulSoup4==4.3.2' )
    echo "-------------------------------------------------------------------------------";
    echo "Installing django-simple-history"
    echo "";
    ( set -x; $sh_c 'pip install git+https://github.com/treyhunner/django-simple-history.git@0fd9b8e9c6f36b0141367b502420efe92d4e21ce' )

    echo "-------------------------------------------------------------------------------";
    echo "Installing Ishtar sources"
    echo "";

    mkdir -p $full_install_path
    cd $full_install_path
    ( set -x; git clone git://git.proxience.com/git/oook_replace.git 2> /dev/null )
    ( set -x; git clone https://gitlab.com/ishtar/ishtar.git 2> /dev/null )
    cd ishtar
    git fetch 2> /dev/null
    git checkout $version 2> /dev/null

    mkdir -p $etc_path
    echo "PATH="$full_install_path > $etc_path"config"
    echo "DEFAULT_DB="$default_db >> $etc_path"config"
    echo "WEBSERVER="$webserver >> $etc_path"config"
    echo ""
    echo "*******************************************************************************";
    echo "";
    echo "Installation done. Base configuration stored in "$etc_path"config file."
    echo "Next you'll have to create an instance."
    echo "";

}

do_install

