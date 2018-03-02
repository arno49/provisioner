# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.ssh.forward_agent = true
  config.vm.hostname = "vagrant-box"
  config.vm.box = "bento/ubuntu-16.04"
  # config.vm.box = "centos/7"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network :private_network, ip: '10.1.100.11'
  # default ./ mounted to /vagrant
  config.vm.synced_folder "../../", "/mnt/"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.customize ['modifyvm', :id, '--natnet1', '192.168.255.0/24']
    vb.customize ["modifyvm", :id, "--memory", "4096"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "100"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    vb.customize ["modifyvm", :id, "--paravirtprovider", "default"]
    ENV['LC_ALL']="en_US.UTF-8"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo -H su -c "cd /vagrant && ./run -i" vagrant
    sudo bash -c 'cat > /home/vagrant/.bash_profile' << EOF
force_color_prompt=yes

if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# Activate venv
if [ -f ~/.ansible_venv/bin/activate ] ; then
  source ~/.ansible_venv/bin/activate
fi

cd /vagrant
echo -e "$(tput bold)╔════════════════════════════════════════════════════════════════════╗$(tput sgr0)"
echo -e "$(tput bold)║                      Ansible testing environment                   ║$(tput sgr0)"
echo -e "$(tput bold)║                                                                    ║$(tput sgr0)"
echo -e "$(tput bold)║             Your upper directory  mounted to /mnt/                 ║$(tput sgr0)"
echo -e "$(tput bold)║             Use wrapper to run ansible playbook:                   ║$(tput sgr0)"
echo -e "$(tput bold)║             ./run -p playbooks/base/bake-nginx.yml                 ║$(tput sgr0)"
echo -e "$(tput bold)║                                                                    ║$(tput sgr0)"
echo -e "$(tput bold)╚════════════════════════════════════════════════════════════════════╝$(tput sgr0)"

EOF
  sudo chown vagrant.vagrant /home/vagrant/.bash_profile
  SHELL
end
