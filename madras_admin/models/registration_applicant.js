'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant', {
    'password': {
      type: DataTypes.STRING,
    },
    'first_name': {
      type: DataTypes.STRING,
    },
    'last_name': {
      type: DataTypes.STRING,
    },
    'github_user_name': {
      type: DataTypes.STRING,
    },
    'email': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'registration_applicant',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

