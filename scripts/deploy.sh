#!/bin/bash

# Install MPI from the sources
function install_cppunit_from_src() {
    local cppunit_install_dir=$1
    message "---> Installs cppunit" -1
    mkdir -p ${cppunit_install_dir}
    local log_file=${log_dir}/install_cppunit

    # extract
    ${third_parties_dir}/uranie/extract-cppunit-1.12.1.sh ${tmp_dir} >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "extract in ${tmp_dir} ..."

    local cppunit_build_dir=${tmp_dir}/cppunit-1.12.1
    # configure
    (cd ${cppunit_build_dir} && ./configure --prefix=${cppunit_install_dir}) >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "configure from ${cppunit_build_dir} ..."
    # make
    (cd ${cppunit_build_dir} && make -j $(nproc)) >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "make from ${cppunit_build_dir} ..."
    # install
    (cd ${cppunit_build_dir} && make -j $(nproc) install) >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "make install from ${cppunit_build_dir} ..."

    message "installed cppunit-1.12.1 in ${cppunit_install_dir} : done (log file in ${log_file}.log)" $?

}

# Install uranie from the archive
function install_uranie_from_src() {
    local uranie_install_dir=$1

    # if ! cppunit-config --version; then
        install_cppunit_from_src ${install_dir}
    # fi

    message "---> Installs uranie-${uranie_version}" -1
    mkdir -p ${uranie_install_dir}
    local log_file=${log_dir}/install_uranie

    # extract
    ${third_parties_dir}/uranie/extract-uranie-${uranie_version}.sh ${tmp_dir} >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "extract in ${tmp_dir} ..."

    local uranie_source_dir=${tmp_dir}/URANIE-${uranie_version}-Source
    local uranie_build_dir=${tmp_dir}/URANIE-${uranie_version}-build
    mkdir -p ${uranie_build_dir}
    # configure
    if [[ "${platform}" == "centos-7" ]]; then
        (cd ${uranie_build_dir} && cmake3 "${uranie_source_dir}" -DCMAKE_BUILD_TYPE='Release' -DCMAKE_INSTALL_PREFIX="${uranie_install_dir}") >> ${log_file}.log 2>> ${log_file}.err &
    else
        (cd ${uranie_build_dir} && cmake "${uranie_source_dir}" -DCMAKE_BUILD_TYPE='Release' -DCMAKE_INSTALL_PREFIX="${uranie_install_dir}") >> ${log_file}.log 2>> ${log_file}.err &
    fi
    wait_process $! "cmake from ${uranie_build_dir} ..."

    # make
    (cd ${uranie_build_dir} && make -j "$(nproc)") >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "make from ${uranie_build_dir} ..."
    # install
    (cd ${uranie_build_dir} && make -j "$(nproc)" install) >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "make install from ${uranie_build_dir} ..."

    message "installed uranie-${uranie_version} in ${uranie_install_dir} : done (log file in ${log_file}.log)" $?
}

root_version='6.24.06'
# Install root from the archive
function install_root_from_package() {
    local root_install_dir=$1
    message "---> Installs root-${root_version}" -1
    mkdir -p ${root_install_dir}
    local log_file=${log_dir}/install_root
    ${third_parties_dir}/root/${platform}/extract-root-${root_version}.sh ${root_install_dir} >> ${log_file}.log 2>> ${log_file}.err &
    wait_process $! "extract in ${tmp_dir} ..."
}

function download_root(){
    message "---> Downloads root" -1
    local log_file=${log_dir}/pip_download_root
    local archive_name=${download_dir}/root/${platform}/root-${root_version}.tar.gz
    mkdir -p ${download_dir}/root/${platform}
    if [[ "${platform}" == "centos-7" ]]; then
        wget https://root.cern/download/root_v${root_version}.Linux-centos7-x86_64-gcc4.8.tar.gz -O ${archive_name} > ${log_file}.log 2> ${log_file}.err &
        wait_process $! "wget root in ${archive_name} ..."
        message "done (log file in ${log_file}.log)" $?
    else
        message "Download of root on ${platform} not implemented." 1
    fi
    _add_extract_script ${archive_name} "root" ${root_version}
}

function download_uranie(){
    message "---> Downloads uranie" -1
    local log_file=${log_dir}/pip_download_uranie
    local archive_name=${download_dir}/uranie/uranie-${uranie_version}.tar.gz
    mkdir -p ${download_dir}/uranie
    wget https://sourceforge.net/projects/uranie/files/URANIE-${uranie_version}-Source.tar.gz -O ${archive_name} > ${log_file}.log 2> ${log_file}.err &
    wait_process $! "wget uranie in ${archive_name} ..."
    message "done (log file in ${log_file}.log)" $?
    _add_extract_script ${archive_name} "uranie" ${uranie_version}

    message "---> Downloads cppunit" -1
    local log_file=${log_dir}/pip_download_cppunit
    local archive_name=${download_dir}/uranie/cppunit-1.12.1.tar.gz
    mkdir -p ${download_dir}/uranie
    wget https://sourceforge.net/projects/cppunit/files/cppunit/1.12.1/cppunit-1.12.1.tar.gz -O ${archive_name} > ${log_file}.log 2> ${log_file}.err &
    wait_process $! "wget cppunit in ${archive_name} ..."
    message "done (log file in ${log_file}.log)" $?
    _add_extract_script ${archive_name} "cppunit" "1.12.1"
}

this_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
root_dir="$(dirname ${this_script_dir})"
work_dir=${PWD}

venv_dir=${this_script_dir}/.venv_utils

uranie_bash_source="/home/uranie-public/uranie-v4.7.0.bashrc"

if [[ -d "${venv_dir}" ]]; then
    if [[ -d "${venv_dir}_old" ]]; then
        rm -rf ${venv_dir}_old
    fi
    mv ${venv_dir} ${venv_dir}_old
fi

python3 -m venv "${venv_dir}"
echo ". ${uranie_bash_source}" >> ${venv_dir}/bin/activate

. ${venv_dir}/bin/activate

pip install --upgrade pip setuptools

pip install -e ${root_dir}[dev]
