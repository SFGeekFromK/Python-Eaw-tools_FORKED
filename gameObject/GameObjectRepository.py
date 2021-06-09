from gameObject.planet import Planet
from gameObject.campaign import Campaign
import os, sys, lxml.etree as et, pickle, shutil
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
def serialize(gameObjectRepo):
    '''some pickle stuff'''

class ModRepository:
    def __init__(self, mod_directory):
        self.mod_dir = mod_directory
        self.game_object_files = self.get_game_object_files()
        self.campaign_files = self.get_galactic_conquests()
        self.hardpoint_files = self.get_hardpoint_files()
        self.tradeRoute_files = self.get_trade_routes()

        self.planets = []
        self.units = {}
        self.hardpoints = {}
        self.text = {}
        self.campaigns = {}

        self.dir = mod_directory
        self.init_repo()
    def get_trade_routes(self):
        tradeRoute_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        tradeRouteFiles = et.parse(self.mod_dir+xmlPath+'/traderoutefiles.xml')
        for child in tradeRouteFiles.getroot():
            if child.tag == 'File':
                tradeRoute_files.append(self.mod_dir+xmlPath+child.text)
        return tradeRoute_files
    def get_hardpoint_files(self):
        hardPoint_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        hardpointdatafiles = et.parse(self.mod_dir+xmlPath+'/hardpointdatafiles.xml')
        for child in hardpointdatafiles.getroot():
            if child.tag == 'File':
                hardPoint_files.append(self.mod_dir+xmlPath+child.text)
        return hardPoint_files
    def get_game_object_files(self):
        game_object_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        gameObjectFiles = et.parse(self.mod_dir+xmlPath+'/gameobjectfiles.xml')
        for child in gameObjectFiles.getroot():
            if child.tag == 'File':
                game_object_files.append(self.mod_dir+xmlPath+child.text)
        return game_object_files
    def get_galactic_conquests(self):
        campaign_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        campaignFiles = et.parse(self.mod_dir+xmlPath+'/campaignfiles.xml')
        for child in campaignFiles.getroot():
            if child.tag == 'File':
                campaign_files.append(self.mod_dir+xmlPath+child.text)
        return campaign_files
    def init_repo(self):
        for file in self.game_object_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Planet':
                    self.planets.append(Planet(child))
        for file in self.campaign_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Campaign':
                    print(child.get('Name'))
                    self.campaigns[child.get('Name')] = Campaign(child, self.planets)
    def update_ui(self, ui):
        for name, campaign in self.campaigns.items():
            ui.select_GC.addItem(name)
            ui.map.plotGalaxy(campaign.planets, [], self.planets)
        for planet in self.planets:
            if planet.name == 'Lehon':
                self.__planetsScatter = ui.map.axes.scatter([planet.x], [planet.y], c = 'b', alpha = 0.1)
            rowCount = ui.planet_list.rowCount()
            ui.planet_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(planet.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            ui.planet_list.setItem(rowCount, 0, item)
        
