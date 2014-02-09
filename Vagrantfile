# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"
  config.vm.network :forwarded_port, guest: 80, host: 8081
  config.vm.network :forwarded_port, guest: 8000, host: 8001

  config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "cookbooks"
      chef.add_recipe "apt"
      chef.add_recipe "python"
      chef.add_recipe "apache2"
      chef.add_recipe "build-essential"
      chef.add_recipe "git"
      chef.add_recipe "mysql"
  end

  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

end
