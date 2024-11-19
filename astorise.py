/****
* Assets
****/
LK.init.shape('enemy', {width:100, height:100, color:0x990789, shape:'box'})
LK.init.shape('hero', {width:100, height:100, color:0x762cde, shape:'box'})
LK.init.shape('heroBullet', {width:100, height:100, color:0x3efde1, shape:'box'})

/**** 
* Classes
****/
// Enemy class
var Enemy = Container.expand(function () {
	var self = Container.call(this);
	var enemyGraphics = self.attachAsset('enemy', {
		anchorX: 0.5,
		anchorY: 0.5
	});
	self.speed = 5;
	self.update = function () {
		self.y += self.speed;
		if (self.y > 2732 + enemyGraphics.height) {
			self.destroy();
			enemies.splice(enemies.indexOf(self), 1);
		}
	};
});
//<Assets used in the game will automatically appear here>
// Hero class
var Hero = Container.expand(function () {
	var self = Container.call(this);
	var heroGraphics = self.attachAsset('hero', {
		anchorX: 0.5,
		anchorY: 0.5
	});
	self.speed = 10;
	self.update = function () {
		// Update logic for hero
		if (LK.isKeyDown('ArrowLeft')) {
			self.x -= self.speed;
		}
		if (LK.isKeyDown('ArrowRight')) {
			self.x += self.speed;
		}
	};
	self.shoot = function () {
		var bullet = new HeroBullet();
		bullet.x = self.x;
		bullet.y = self.y - heroGraphics.height / 2;
		game.addChild(bullet);
		heroBullets.push(bullet);
	};
});
// HeroBullet class
var HeroBullet = Container.expand(function () {
	var self = Container.call(this);
	var bulletGraphics = self.attachAsset('heroBullet', {
		anchorX: 0.5,
		anchorY: 0.5
	});
	self.speed = -15;
	self.update = function () {
		self.y += self.speed;
		if (self.y < -bulletGraphics.height) {
			self.destroy();
			heroBullets.splice(heroBullets.indexOf(self), 1);
		}
	};
});

/**** 
* Initialize Game
****/
var game = new LK.Game({
	backgroundColor: 0x000000 //Init game with black background 
});

/**** 
* Game Code
****/
var hero;
var heroBullets = [];
var enemies = [];
var score = 0;
var scoreTxt;
// Initialize hero
hero = new Hero();
hero.x = 2048 / 2;
hero.y = 2732 - 200;
game.addChild(hero);
// Initialize score text
scoreTxt = new Text2('0', {
	size: 150,
	fill: "#ffffff"
});
scoreTxt.anchor.set(0.5, 0);
LK.gui.top.addChild(scoreTxt);
// Handle game updates
game.update = function () {
	// Update hero bullets
	for (var i = heroBullets.length - 1; i >= 0; i--) {
		heroBullets[i].update();
	}
	// Update enemies
	for (var j = enemies.length - 1; j >= 0; j--) {
		enemies[j].update();
		if (enemies[j].intersects(hero)) {
			LK.effects.flashScreen(0xff0000, 1000);
			LK.showGameOver();
		}
	}
	// Spawn enemies
	if (LK.ticks % 60 == 0) {
		var enemy = new Enemy();
		enemy.x = Math.random() * 2048;
		enemy.y = -100;
		game.addChild(enemy);
		enemies.push(enemy);
	}
	// Check for bullet-enemy collisions
	for (var k = heroBullets.length - 1; k >= 0; k--) {
		for (var l = enemies.length - 1; l >= 0; l--) {
			if (heroBullets[k].intersects(enemies[l])) {
				heroBullets[k].destroy();
				enemies[l].destroy();
				heroBullets.splice(k, 1);
				enemies.splice(l, 1);
				score++;
				scoreTxt.setText(score);
				break;
			}
		}
	}
};
// Handle touch events
LK.on('keydown', function (key) {
	if (key === 'ArrowLeft' || key === 'ArrowRight') {
		hero.update();
	}
});
LK.on('keyup', function (key) {
	if (key === 'ArrowLeft' || key === 'ArrowRight') {
		hero.update();
	}
});
game.down = function (x, y, obj) {
	hero.shoot();
};
game.move = function (x, y, obj) {
	hero.x = x;
};
game.up = function (x, y, obj) {
	// No action needed on touch up
};
