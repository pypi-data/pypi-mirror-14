class portfolio_materialize:
	def __init__(self, f, arg):
		print 'getting started'
		self.f = f
		self.arg = arg
		self.set_values()
		self.build_page()

	def set_values(self):
		print "I'm going to ask you several questions if you don't wish to answer just press enter as you go"
		self.name = raw_input('What is your name?')
		self.email = raw_input('what is your email?')
		self.socialMedia()
		self.quote()
		self.resume()

	def socialMedia(self):
		self.facebook = raw_input('what is your facebook link?')
		self.linkedin = raw_input('what is your linkedin link?')
		self.twitter = raw_input('what is your twitter link?')
		self.google = raw_input('what is your google link?')

	def quote(self):
		quote = raw_input('Do you have an inspirational quote? yes or no\n')
		if quote == 'yes':
			self.quote = raw_input("What is your quote?\n")
		elif quote == 'no':
			self.quote = "I had no interesting quote to provide"
		else: 
			self.quote()

	def resume(self):
		resume = raw_input('Do you have a link to a resume download? yes or no\n')
		if resume == 'yes':
			self.resume = raw_input('Provide a link to your resume.')
		elif resume == 'no':
			self.resume = False
		else:
			self.resume()

	def build_page(self):
		self.build_nav()
  		self.f.write('\t<div id="index-banner" class="parallax-container">\n \t\t<div class="section no-pad-bot">\n \t\t\t<div class="container">\n \t\t\t<br><br>\n \t\t\t\t<h1 class="header center teal-text text-lighten-2">{name}</h1>\n \t\t\t\t<div class="row center">\n \t\t\t\t\t<h5 class="header col s12 light">{quote}</h5>\n \t\t\t\t</div>\n \t\t\t\t<div class="row center">\n \t\t\t\t\t<a href="{resume_link}" id="download-button" class="btn-large waves-effect waves-light teal lighten-1">Resume</a>\n \t\t\t\t</div>\n \t\t\t\t<br><br>\n \t\t\t</div>\n \t\t</div>\n \t\t<div class="parallax"><img src="background1.jpg" alt="Unsplashed background img 1"></div>\n \t</div>\n \t<div class="container">\n \t\t<div class="section">\n \t\t\t<!--   Icon Section   -->\n \t\t\t<div class="row">\n \t\t\t\t<div class="col s12 m4">\n \t\t\t\t\t<div class="icon-block">\n \t\t\t\t\t\t<h2 class="center brown-text"><i class="material-icons">flash_on</i></h2>\n \t\t\t\t\t\t<h5 class="center">Speeds up development</h5>\n \t\t\t\t\t\t<p class="light">We did most of the heavy lifting for you to provide a default stylings that incorporate our custom components. Additionally, we refined animations and transitions to provide a smoother experience for developers.</p>\n \t\t\t\t\t</div>\n \t\t\t\t</div>\n \t\t\t\t<div class="col s12 m4">\n \t\t\t\t\t<div class="icon-block">\n \t\t\t\t\t\t<h2 class="center brown-text"><i class="material-icons">group</i></h2>\n \t\t\t\t\t\t<h5 class="center">User Experience Focused</h5>\n \t\t\t\t\t\t<p class="light">By utilizing elements and principles of Material Design, we were able to create a framework that incorporates components and animations that provide more feedback to users. Additionally, a single underlying responsive system across all platforms allow for a more unified user experience.</p>\n \t\t\t\t\t</div>\n \t\t\t\t</div>\n \t\t\t\t<div class="col s12 m4">\n \t\t\t\t\t<div class="icon-block">\n \t\t\t\t\t\t<h2 class="center brown-text"><i class="material-icons">settings</i></h2>\n \t\t\t\t\t\t<h5 class="center">Easy to work with</h5>\n \t\t\t\t\t\t<p class="light">We have provided detailed documentation as well as specific code examples to help new users get started. We are also always open to feedback and can answer any questions a user may have about Materialize.</p>\n \t\t\t\t\t</div>\n \t\t\t\t</div>\n \t\t\t</div>\n \t\t</div>\n \t</div>\n \t<div class="parallax-container valign-wrapper">\n \t\t<div class="section no-pad-bot">\n \t\t\t<div class="container">\n \t\t\t\t<div class="row center">\n \t\t\t\t\t<h5 class="header col s12 light">A modern responsive front-end framework based on Material Design</h5>\n \t\t\t\t</div>\n \t\t\t</div>\n \t\t</div>\n \t\t<div class="parallax"><img src="background2.jpg" alt="Unsplashed background img 2"></div>\n \t</div>\n \t<div class="container">\n \t\t<div class="section">\n \t\t\t<div class="row">\n \t\t\t\t<div class="col s12 center">\n \t\t\t\t\t<h3><i class="mdi-content-send brown-text"></i></h3>\n \t\t\t\t\t<h4>Contact Us</h4>\n \t\t\t\t\t<p class="left-align light">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque id nunc nec volutpat. Etiam pellentesque tristique arcu, non consequat magna fermentum ac. Cras ut ultricies eros. Maecenas eros justo, ullamcorper a sapien id, viverra ultrices eros. Morbi sem neque, posuere et pretium eget, bibendum sollicitudin lacus. Aliquam eleifend sollicitudin diam, eu mattis nisl maximus sed. Nulla imperdiet semper molestie. Morbi massa odio, condimentum sed ipsum ac, gravida ultrices erat. Nullam eget dignissim mauris, non tristique erat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;</p>\n \t\t\t\t</div>\n \t\t\t</div>\n \t\t</div>\n \t</div>\n \t<div class="parallax-container valign-wrapper">\n \t\t<div class="section no-pad-bot">\n \t\t\t<div class="container">\n \t\t\t\t<div class="row center">\n \t\t\t\t\t<h5 class="header col s12 light">A modern responsive front-end framework based on Material Design</h5>\n \t\t\t\t</div>\n \t\t\t</div>\n \t\t</div>\n \t\t<div class="parallax"><img src="background3.jpg" alt="Unsplashed background img 3"></div>\n \t</div>\n'.format(name=self.name, quote=self.quote, resume_link = self.resume, facebook = self.facebook, linkedin = self.linkedin, google = self.google, twitter = self.twitter))
  		self.build_footer()

  	def build_nav(self):
		self.f.write('\t<nav class="white" role="navigation">\n\t\t<div class="nav-wrapper container">\n\t\t\t<a id="logo-container" href="#" class="brand-logo">{name}</a>\n\t\t\t<ul class="right hide-on-med-and-down">\n\t\t\t\t<li><a href="#">Navbar Link</a></li>\n\t\t\t</ul>\n\t\t\t<ul id="nav-mobile" class="side-nav">\n\t\t\t\t<li><a href="#">Navbar Link</a></li>\n\t\t\t</ul>\n\t\t\t<a href="#" data-activates="nav-mobile" class="button-collapse"><i class="material-icons">menu</i></a>\n\t\t</div>\n\t</nav>\n'.format(name=self.name))

	def build_footer(self):
		self.f.write('\t<footer class="page-footer teal">\n \t\t<div class="container">\n \t\t\t<div class="row">\n \t\t\t\t<div class="col l6 s12">\n \t\t\t\t\t<h5 class="white-text">Mission Statement</h5>\n \t\t\t\t\t<p class="grey-text text-lighten-4">{quote}</p>\n\t\t\t\t</div>\n \t\t\t\t<div class="col l3 s12">\n \t\t\t\t\t<h5 class="white-text">Settings</h5>\n \t\t\t\t\t<ul>\n \t\t\t\t\t\t<li><a class="white-text" href="#!">Link 1</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="#!">Link 2</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="#!">Link 3</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="#!">Link 4</a></li>\n \t\t\t\t\t</ul>\n \t\t\t\t</div>\n \t\t\t\t<div class="col l3 s12">\n \t\t\t\t\t<h5 class="white-text">Connect</h5>\n \t\t\t\t\t<ul>\n \t\t\t\t\t\t<li><a class="white-text" href="{facebook}">Facebook</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="{linkedin}">Linkedin</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="{google}">Google+</a></li>\n \t\t\t\t\t\t<li><a class="white-text" href="{twitter}">Twitter</a></li>\n \t\t\t\t\t</ul>\n \t\t\t\t</div>\n \t\t\t</div>\n \t\t</div>\n \t\t<div class="footer-copyright">\n \t\t\t<div class="container">\n Made by <a class="brown-text text-lighten-3" href="http://materializecss.com">Materialize</a>\n \t\t\t</div>\n \t\t</div>\n \t</footer>\n'.format(name=self.name, quote=self.quote, resume_link = self.resume, facebook = self.facebook, linkedin = self.linkedin, google = self.google, twitter = self.twitter))


